import { constants } from "node:fs"
import { open, readFile } from "node:fs/promises"
import path from "node:path"

import { tool } from "@opencode-ai/plugin"

const MANIFEST_RELATIVE_PATH = ".agent-input/translation-segments.json"
const RESULT_RELATIVE_PATH = ".tmp/generative-translation.ko.segments.jsonl"
const TOKEN_RE = /⟦ARA\d{4}⟧/g
const MAX_BATCH = 24
const MAX_TEXT_BYTES = 16 * 1024
const MAX_RESULT_BYTES = 1024 * 1024
let writeQueue = Promise.resolve()
const submitted = new Set<string>()

async function withExclusiveWrite<T>(operation: () => Promise<T>): Promise<T> {
  let release!: () => void
  const previous = writeQueue
  writeQueue = new Promise<void>((resolve) => {
    release = resolve
  })
  await previous
  try {
    return await operation()
  } finally {
    release()
  }
}

type ManifestSegment = { id: string; tokens: string[]; forbid_commas: boolean }
type Manifest = { version: number; segment_count: number; segments: ManifestSegment[] }

async function loadManifest(worktree: string): Promise<Manifest> {
  const raw = await readFile(path.join(worktree, MANIFEST_RELATIVE_PATH), "utf8")
  const manifest = JSON.parse(raw) as Manifest
  if (
    manifest.version !== 1 ||
    !Number.isInteger(manifest.segment_count) ||
    !Array.isArray(manifest.segments) ||
    manifest.segments.length !== manifest.segment_count
  ) {
    throw new Error("translation segment manifest is malformed")
  }
  return manifest
}

export default tool({
  description:
    "Submit Korean translations for fixed text segment ids. Opaque ARA tokens must remain exact and ordered.",
  args: {
    segments: tool.schema
      .array(
        tool.schema.object({
          id: tool.schema.string().regex(/^s\d{5}$/),
          text: tool.schema.string().min(1),
        }),
      )
      .min(1)
      .max(MAX_BATCH),
  },
  async execute(args, context) {
    return withExclusiveWrite(async () => {
      const manifest = await loadManifest(context.worktree)
      const allowed = new Map(
        manifest.segments.map(
          (segment): [string, ManifestSegment] => [segment.id, segment],
        ),
      )
      const batchIds = new Set<string>()
      let batchBytes = 0
      const lines: string[] = []
      for (const segment of args.segments) {
        if (batchIds.has(segment.id) || submitted.has(segment.id)) {
          throw new Error(`duplicate translation segment: ${segment.id}`)
        }
        const expected = allowed.get(segment.id)
        if (!expected) throw new Error(`unknown translation segment: ${segment.id}`)
        const actualTokens = segment.text.match(TOKEN_RE) ?? []
        if (JSON.stringify(actualTokens) !== JSON.stringify(expected.tokens)) {
          throw new Error(`immutable token mismatch for ${segment.id}`)
        }
        if (expected.forbid_commas && segment.text.includes(",")) {
          throw new Error(`unprotected list separator in ${segment.id}`)
        }
        const line = JSON.stringify({ id: segment.id, text: segment.text }) + "\n"
        batchBytes += Buffer.byteLength(line, "utf8")
        if (batchBytes > MAX_TEXT_BYTES) throw new Error(`batch exceeds ${MAX_TEXT_BYTES} UTF-8 bytes`)
        batchIds.add(segment.id)
        lines.push(line)
      }

      const resultPath = path.join(context.worktree, RESULT_RELATIVE_PATH)
      const first = submitted.size === 0
      const flags = first
        ? constants.O_WRONLY | constants.O_CREAT | constants.O_EXCL | constants.O_NOFOLLOW
        : constants.O_WRONLY | constants.O_APPEND | constants.O_NOFOLLOW
      const handle = await open(resultPath, flags, 0o600)
      try {
        const before = await handle.stat()
        if (!before.isFile()) throw new Error("translation result is not a regular file")
        if (before.size + batchBytes > MAX_RESULT_BYTES) {
          throw new Error(`translation result exceeds ${MAX_RESULT_BYTES} bytes`)
        }
        await handle.writeFile(lines.join(""), { encoding: "utf8" })
        await handle.sync()
      } finally {
        await handle.close()
      }
      for (const id of batchIds) submitted.add(id)
      const remaining = manifest.segment_count - submitted.size
      return remaining === 0
        ? `All ${manifest.segment_count} translation segments accepted.`
        : `Batch accepted. ${remaining} of ${manifest.segment_count} segments remain.`
    })
  },
})

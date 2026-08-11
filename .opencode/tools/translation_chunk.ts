import { constants } from "node:fs"
import { open } from "node:fs/promises"
import path from "node:path"

import { tool } from "@opencode-ai/plugin"

const DRAFT_RELATIVE_PATH = ".tmp/generative-translation.ko.ara.md"
const MAX_CHUNK_BYTES = 16 * 1024
const MAX_DRAFT_BYTES = 1024 * 1024
let writeQueue = Promise.resolve()

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

export default tool({
  description:
    "Append the next UTF-8 chunk of the Korean translation to the one fixed draft. " +
    "Start with offset_bytes=0, then use the exact next offset returned by each call.",
  args: {
    offset_bytes: tool.schema.number().int().nonnegative(),
    content: tool.schema.string().min(1),
  },
  async execute(args, context) {
    return withExclusiveWrite(async () => {
      const chunkBytes = Buffer.byteLength(args.content, "utf8")
      if (chunkBytes > MAX_CHUNK_BYTES) {
        throw new Error(`chunk exceeds ${MAX_CHUNK_BYTES} UTF-8 bytes`)
      }

      const draftPath = path.join(context.worktree, DRAFT_RELATIVE_PATH)
      const flags =
        args.offset_bytes === 0
          ? constants.O_WRONLY | constants.O_CREAT | constants.O_EXCL | constants.O_NOFOLLOW
          : constants.O_WRONLY | constants.O_APPEND | constants.O_NOFOLLOW
      const handle = await open(draftPath, flags, 0o600)
      try {
        const before = await handle.stat()
        if (!before.isFile()) throw new Error("translation draft is not a regular file")
        if (before.size !== args.offset_bytes) {
          throw new Error(
            `offset mismatch: draft is ${before.size} bytes, got ${args.offset_bytes}`,
          )
        }
        if (before.size + chunkBytes > MAX_DRAFT_BYTES) {
          throw new Error(`translation draft exceeds ${MAX_DRAFT_BYTES} bytes`)
        }
        await handle.writeFile(args.content, { encoding: "utf8" })
        await handle.sync()
        const after = await handle.stat()
        if (after.size !== before.size + chunkBytes) {
          throw new Error("translation chunk write was incomplete")
        }
        return `Chunk accepted. next offset_bytes=${after.size}`
      } finally {
        await handle.close()
      }
    })
  },
})

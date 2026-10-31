#!/usr/bin/env node
// PreToolUse guard for run-claude-container: an exact path ALLOWLIST for the
// built-in file tools, derived from the run-scoped settings' permissions.allow.
//
// WHY THIS EXISTS
//
// Claude Code's dontAsk mode still runs every read inside the working
// directory without consulting any rule, and an allow rule can only widen,
// never narrow, what runs. The isolated clone is the whole repository, so
// `Read(.agent-input/aradio/**)` alone would not stop a prompt-injected read
// of any other file. This hook closes that gap: a Read, Write, or Edit call
// proceeds only when its canonical target matches an allow rule, and every
// other tool is refused outright.
//
// It never grants anything. Exit 0 with no output defers to the normal
// permission flow (restricted mode, deny rules, dontAsk). Exit 2 blocks the
// call before any permission rule is evaluated. The settings hook command
// appends `|| exit 2`, so a crash or a missing interpreter blocks too.
//
// Rule grammar, kept identical to scripts/copy_claude_settings.py: `Read(p)`
// or `Edit(p)`, where p is a clean workspace-relative path, optionally ending
// in `/**`. Anything else fails closed.

import { lstatSync, readFileSync, realpathSync } from "node:fs";
import path from "node:path";

const RULE = /^(Read|Edit)\(([A-Za-z0-9_.-]+(?:\/[A-Za-z0-9_.-]+)*)(\/\*\*)?\)$/;
const MAX_INPUT_BYTES = 32 * 1024 * 1024;
// The only tools this adapter may expose; each names the input field that
// holds its target and the rule kind that governs it.
const FILE_TOOLS = {
  Read: { field: "file_path", kind: "Read" },
  Write: { field: "file_path", kind: "Edit" },
  Edit: { field: "file_path", kind: "Edit" },
};

function deny(reason) {
  process.stderr.write(`ARA tool guard denied this call: ${reason}\n`);
  process.exit(2);
}

function loadRules(settingsPath) {
  let settings;
  try {
    settings = JSON.parse(readFileSync(settingsPath, "utf8"));
  } catch {
    deny("the run-scoped settings file is unreadable");
  }
  const allow = settings?.permissions?.allow;
  if (!Array.isArray(allow)) {
    deny("the run-scoped settings have no permissions.allow list");
  }
  const rules = [];
  for (const entry of allow) {
    const match = typeof entry === "string" ? RULE.exec(entry) : null;
    if (!match) {
      deny("the run-scoped settings contain an unsupported allow rule");
    }
    const target = match[2];
    if (target.split("/").some((part) => part === "." || part === "..")) {
      deny("the run-scoped settings contain a traversing allow rule");
    }
    rules.push({ kind: match[1], target, prefix: Boolean(match[3]) });
  }
  return rules;
}

function canonicalWorkspace(workspace) {
  if (typeof workspace !== "string" || !path.isAbsolute(workspace)) {
    deny("the workspace root is not absolute");
  }
  const resolved = path.resolve(workspace);
  let real;
  try {
    real = realpathSync(resolved);
  } catch {
    deny("the workspace root does not exist");
  }
  if (real !== resolved) {
    deny("the workspace root is not canonical");
  }
  return resolved;
}

// Resolve the requested path without following any symlink: the target, or
// for a file that does not exist yet its nearest existing ancestor, must
// already be canonical. A write may create missing parent directories, which
// cannot be links because they do not exist.
function canonicalTarget(requested, workspace, mustExist) {
  if (typeof requested !== "string" || requested === "" || requested.includes("\0")) {
    deny("the tool call has no usable file path");
  }
  const absolute = path.resolve(workspace, requested);
  let probe = absolute;
  let stat = null;
  while (stat === null) {
    try {
      stat = lstatSync(probe);
    } catch (error) {
      if (mustExist || error?.code !== "ENOENT") {
        deny("the target does not exist or cannot be inspected");
      }
      const parent = path.dirname(probe);
      if (parent === probe) {
        deny("the target has no existing ancestor");
      }
      probe = parent;
    }
  }
  if (probe === absolute ? !stat.isFile() : !stat.isDirectory()) {
    deny("the target is not a regular file under a directory");
  }
  let real;
  try {
    real = realpathSync(probe);
  } catch {
    deny("the target cannot be canonicalized");
  }
  if (real !== probe) {
    deny("the target path crosses a symlink");
  }
  const relative = path.relative(workspace, absolute);
  if (relative === "" || relative.startsWith("..") || path.isAbsolute(relative)) {
    deny("the target is outside the workspace");
  }
  return relative.split(path.sep).join("/");
}

function allowed(rules, kind, relative) {
  return rules.some((rule) => rule.kind === kind && (
    rule.prefix ? relative.startsWith(`${rule.target}/`) : relative === rule.target
  ));
}

function main() {
  const [settingsPath, workspaceArg] = process.argv.slice(2);
  const rules = loadRules(settingsPath);
  const workspace = canonicalWorkspace(workspaceArg);

  let raw;
  try {
    raw = readFileSync(0);
  } catch {
    deny("the hook input is unreadable");
  }
  if (raw.length > MAX_INPUT_BYTES) {
    deny("the hook input is too large");
  }
  let event;
  try {
    event = JSON.parse(raw.toString("utf8"));
  } catch {
    deny("the hook input is not JSON");
  }
  const tool = event?.tool_name;
  const spec = Object.hasOwn(FILE_TOOLS, tool) ? FILE_TOOLS[tool] : null;
  if (!spec) {
    deny(`tool ${JSON.stringify(String(tool)).slice(0, 80)} is not allowed in this lane`);
  }
  const input = event.tool_input;
  if (!input || typeof input !== "object") {
    deny("the tool call has no input object");
  }
  const relative = canonicalTarget(input[spec.field], workspace, spec.kind === "Read");
  if (!allowed(rules, spec.kind, relative)) {
    deny(`${tool} of ${JSON.stringify(relative).slice(0, 200)} is outside this lane's allowlist`);
  }
  process.exit(0);
}

main();

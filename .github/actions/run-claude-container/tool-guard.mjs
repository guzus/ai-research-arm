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
// of any other file. This hook closes that gap: a Read or Write call proceeds
// only when its canonical target matches an allow rule, a Glob only lists a
// directory under a Read rule, a Bash command only in the exact git, curl, and
// uv forms the lane's rules describe, and every other tool, Edit included, is
// refused outright.
//
// It never grants anything. Exit 0 with no output defers to the normal
// permission flow (restricted mode, deny rules, dontAsk). Exit 2 blocks the
// call before any permission rule is evaluated. The settings hook command
// appends `|| exit 2`, so a crash or a missing interpreter (any nonzero exit)
// blocks too. That is NOT fail-closed for every failure: Claude Code 2.1.285
// lets the call proceed when it kills a hook that outlived its timeout, or
// when a signal kills the hook shell itself. scripts/copy_claude_settings.py
// therefore grants this guard a 600 s timeout against a runtime of tens of
// milliseconds; outside /workspace, restricted mode, the deny rules and
// dontAsk still refuse the call on their own.
//
// Every refusal also appends "<tool>\t<reason code>" to the denial log named
// by the fourth argument: a closed set of codes and tool names, never an
// input or a path, so the host can print why a lane was refused without
// echoing untrusted text.
//
// Rule grammar, kept identical to scripts/copy_claude_settings.py: `Read(p)`
// or `Edit(p)` on a clean workspace-relative path, optionally ending in `/**`
// (an Edit rule governs the Write tool); `Glob`; `Bash(git add <dir>/*)`;
// `Bash(git commit -m *)`; `Bash(curl -s "https://<host>/<path>?*)` on a host
// in CURL_HOSTS, never following a redirect; `Bash(uv run python
// scripts/<name>.py)`, optionally with one fixed ` --flag` or ` "*` (one
// quoted plain-text argument). Anything else fails closed. Claude Code still
// applies its own allow and deny rules after this hook defers, so both layers
// must admit a call.

import {
  closeSync, constants, lstatSync, openSync, readFileSync, realpathSync, writeSync,
} from "node:fs";
import path from "node:path";

const RULE = /^(Read|Edit)\(([A-Za-z0-9_.-]+(?:\/[A-Za-z0-9_.-]+)*)(\/\*\*)?\)$/;
const GIT_ADD_RULE = /^Bash\(git add ([A-Za-z0-9_.-]+(?:\/[A-Za-z0-9_.-]+)*)\/\*\)$/;
const GIT_COMMIT_RULE = "Bash(git commit -m *)";
const CURL_RULE = /^Bash\(curl -s "(https:\/\/[a-z0-9]+(?:[.-][a-z0-9]+)*\.[a-z]{2,}(?:\/[A-Za-z0-9_.-]+)*\/?\?)\*\)$/;
const UV_RULE = /^Bash\((uv run python scripts\/([a-z0-9_]+)\.py)( --[a-z][a-z-]*| "\*)?\)$/;
const GLOB_RULE = "Glob";
// The only hosts a curl rule may name, kept identical to CURL_HOSTS in
// scripts/copy_claude_settings.py: reaching a new host is a reviewed code
// change, never a policy edit alone.
const CURL_HOSTS = ["export.arxiv.org"];
const MAX_INPUT_BYTES = 32 * 1024 * 1024;
// No glob classes or braces: `{..,x}` would expand to a parent directory.
const GLOB_PATTERN = /^[A-Za-z0-9_.*?-]+(?:\/[A-Za-z0-9_.*?-]+)*$/;
// Shell-inert by construction. A staged path holds no quote, `$`, backtick,
// backslash, `;`, `|`, `&`, `<`, `>`, glob character, `~`, or whitespace. A
// commit message, curl URL, or uv argument sits inside quotes and holds no
// double quote, `$`, backtick, backslash, or `!`, so the shell reads it
// literally.
const STAGE_PATH = /^[A-Za-z0-9_.][A-Za-z0-9_.-]*(?:\/[A-Za-z0-9_.-]+)*\/?$/;
const COMMIT_COMMAND = /^git commit -m (?:"[A-Za-z0-9 :._,()#+\/@-]{1,200}"|'[A-Za-z0-9 :._,()#+\/@-]{1,200}')(?: \|\| echo "No changes")?$/;
const CURL_COMMAND = /^curl -s "([^"]*)"$/;
const URL_QUERY = /^[A-Za-z0-9_=&+:.%,()\/@-]*$/;
const UV_ARGUMENT = /^[A-Za-z0-9 ._,:()\/+'-]{1,200}$/;
// The closed sets the denial log may hold; scripts/summarize_claude_result.py
// keeps the same lists and drops any other line.
const REASONS = new Set([
  "policy_invalid", "workspace_invalid", "input_invalid", "tool_not_allowed",
  "path_invalid", "path_tilde", "path_missing", "path_type", "path_symlink", "path_outside",
  "path_not_allowed", "git_metadata", "glob_pattern", "shell_multiline", "shell_background",
  "shell_metachar", "command_not_allowed", "curl_flag", "curl_form", "curl_url",
  "curl_query", "uv_form", "uv_argument", "git_form", "commit_form",
]);
const LOGGED_TOOLS = new Set([
  "Read", "Write", "Edit", "MultiEdit", "Glob", "Grep", "Bash", "WebFetch", "WebSearch",
  "Task", "Agent", "NotebookEdit", "TodoWrite", "Skill",
]);

let denialLog = null;
let toolName = null;

function loggedTool() {
  if (typeof toolName !== "string") {
    return "-";
  }
  if (LOGGED_TOOLS.has(toolName)) {
    return toolName;
  }
  return toolName.startsWith("mcp__") ? "mcp" : "other";
}

function deny(code, reason) {
  process.stderr.write(`ARA tool guard denied this call: ${reason}\n`);
  if (typeof denialLog === "string" && path.isAbsolute(denialLog)) {
    try {
      const fd = openSync(denialLog,
        constants.O_WRONLY | constants.O_APPEND | constants.O_CREAT | constants.O_NOFOLLOW,
        0o600);
      try {
        writeSync(fd, `${loggedTool()}\t${REASONS.has(code) ? code : "policy_invalid"}\n`);
      } finally {
        closeSync(fd);
      }
    } catch {
      // Recording is best effort: the refusal never depends on it.
    }
  }
  process.exit(2);
}

// Shell syntax outside every quoted span: what the shell itself would act on.
function shellSyntax(text) {
  return /[|;&<>`$\\(){}!*?~#]/.test(text.replace(/"[^"]*"|'[^']*'/g, ""));
}

function noTraversal(target) {
  return !target.split("/").some((part) => part === "." || part === "..");
}

function loadPolicy(settingsPath) {
  let settings;
  try {
    settings = JSON.parse(readFileSync(settingsPath, "utf8"));
  } catch {
    deny("policy_invalid", "the run-scoped settings file is unreadable");
  }
  const allow = settings?.permissions?.allow;
  if (!Array.isArray(allow)) {
    deny("policy_invalid", "the run-scoped settings have no permissions.allow list");
  }
  const policy = { files: [], glob: false, gitAdd: [], gitCommit: false, curl: [], uv: [] };
  for (const entry of allow) {
    if (typeof entry !== "string") {
      deny("policy_invalid", "the run-scoped settings contain an unsupported allow rule");
    }
    let match;
    if (entry === GLOB_RULE) {
      policy.glob = true;
    } else if (entry === GIT_COMMIT_RULE) {
      policy.gitCommit = true;
    } else if ((match = RULE.exec(entry))) {
      policy.files.push({ kind: match[1], target: match[2], prefix: Boolean(match[3]) });
    } else if ((match = GIT_ADD_RULE.exec(entry))) {
      policy.gitAdd.push(match[1]);
    } else if ((match = CURL_RULE.exec(entry))) {
      if (!CURL_HOSTS.includes(match[1].slice("https://".length).split(/[/?]/, 1)[0])) {
        deny("policy_invalid", "the run-scoped settings name a curl host outside CURL_HOSTS");
      }
      policy.curl.push({ prefix: match[1] });
    } else if ((match = UV_RULE.exec(entry))) {
      policy.uv.push({ base: match[1], suffix: match[3] ?? "" });
    } else {
      deny("policy_invalid", "the run-scoped settings contain an unsupported allow rule");
    }
    const urlPaths = policy.curl.map((rule) => rule.prefix.slice("https://".length, -1));
    if (![...policy.files.map((rule) => rule.target), ...policy.gitAdd, ...urlPaths]
      .every(noTraversal)) {
      deny("policy_invalid", "the run-scoped settings contain a traversing allow rule");
    }
  }
  return policy;
}

function canonicalWorkspace(workspace) {
  if (typeof workspace !== "string" || !path.isAbsolute(workspace)) {
    deny("workspace_invalid", "the workspace root is not absolute");
  }
  const resolved = path.resolve(workspace);
  let real;
  try {
    real = realpathSync(resolved);
  } catch {
    deny("workspace_invalid", "the workspace root does not exist");
  }
  if (real !== resolved) {
    deny("workspace_invalid", "the workspace root is not canonical");
  }
  return resolved;
}

// Resolve the requested path without following any symlink: the target, or
// for a file that does not exist yet its nearest existing ancestor, must
// already be canonical. A write may create missing parent directories, which
// cannot be links because they do not exist. `expect` is "read" (an existing
// regular file), "write" (a regular file or not yet existing), "list" (an
// existing directory), or "stage" (an existing file or directory).
function canonicalTarget(requested, workspace, expect) {
  if (typeof requested !== "string" || requested === "" || requested.includes("\0")) {
    deny("path_invalid", "the tool call has no usable file path");
  }
  // The CLI expands a leading ~ to HOME before it touches the file, so
  // `~/../.tmp/aradio/edit.json` would pass a check that resolves ~ as a
  // directory name. No lane file name contains ~: refuse it anywhere rather
  // than ever disagree with the CLI about the target.
  if (requested.includes("~")) {
    deny("path_tilde", "the target path contains ~");
  }
  const absolute = path.resolve(workspace, requested);
  let probe = absolute;
  let stat = null;
  while (stat === null) {
    try {
      stat = lstatSync(probe);
    } catch (error) {
      if (expect !== "write" || error?.code !== "ENOENT") {
        deny("path_missing", "the target does not exist or cannot be inspected");
      }
      const parent = path.dirname(probe);
      if (parent === probe) {
        deny("path_missing", "the target has no existing ancestor");
      }
      probe = parent;
    }
  }
  const shapeOk = probe !== absolute ? stat.isDirectory()
    : expect === "list" ? stat.isDirectory()
      : expect === "stage" ? stat.isFile() || stat.isDirectory()
        : stat.isFile();
  if (!shapeOk) {
    deny("path_type", "the target is not the expected regular file or directory");
  }
  let real;
  try {
    real = realpathSync(probe);
  } catch {
    deny("path_symlink", "the target cannot be canonicalized");
  }
  if (real !== probe) {
    deny("path_symlink", "the target path crosses a symlink");
  }
  const relative = path.relative(workspace, absolute);
  if (relative === "" || relative.startsWith("..") || path.isAbsolute(relative)) {
    deny("path_outside", "the target is outside the workspace");
  }
  return relative.split(path.sep).join("/");
}

function fileAllowed(policy, kind, relative) {
  return policy.files.some((rule) => rule.kind === kind && (
    rule.prefix ? relative.startsWith(`${rule.target}/`) : relative === rule.target
  ));
}

// No lane output is git metadata. Under a directory-prefix lane such as
// research/wiki/ a planted .gitattributes would pass the trusted import and
// change how every later checkout filters or converts those files; a nested
// .git is refused there, but never needs to be written either.
function gitMetadata(relative) {
  return relative.split("/").some((part) => part.toLowerCase().startsWith(".git"));
}

function within(directories, relative) {
  return directories.some((dir) => relative === dir || relative.startsWith(`${dir}/`));
}

function checkGlob(policy, input, workspace) {
  if (!policy.glob) {
    deny("tool_not_allowed", "tool \"Glob\" is not allowed in this lane");
  }
  const { pattern } = input;
  if (typeof pattern !== "string" || !GLOB_PATTERN.test(pattern) || !noTraversal(pattern)) {
    deny("glob_pattern",
      "the Glob pattern must be a plain relative pattern (no braces, classes, .., or ~)");
  }
  const segments = pattern.split("/");
  const literal = [];
  for (const segment of segments) {
    if (/[*?]/.test(segment)) {
      break;
    }
    literal.push(segment);
  }
  // A pattern without wildcards names one entry: list its directory.
  if (literal.length === segments.length) {
    literal.pop();
  }
  const base = input.path === undefined ? "." : input.path;
  if (typeof base !== "string" || base === "") {
    deny("path_invalid", "the Glob path is not usable");
  }
  if (base.includes("~")) {
    deny("path_tilde", "the Glob path contains ~");
  }
  const directory = path.join(path.resolve(workspace, base), ...literal);
  const relative = canonicalTarget(directory, workspace, "list");
  const readDirs = policy.files.filter((rule) => rule.kind === "Read" && rule.prefix)
    .map((rule) => rule.target);
  if (!within(readDirs, relative)) {
    deny("path_not_allowed",
      `Glob under ${JSON.stringify(relative).slice(0, 200)} is outside this lane's allowlist`);
  }
}

function checkGitAdd(policy, segment, workspace) {
  const words = segment.split(" ");
  if (!policy.gitAdd.length) {
    deny("command_not_allowed", "this lane does not stage files");
  }
  if (words.length < 3 || words[0] !== "git" || words[1] !== "add") {
    deny("git_form", "this lane stages only with `git add <path>...` under its own write paths");
  }
  for (const word of words.slice(2)) {
    if (!STAGE_PATH.test(word) || !noTraversal(word.replace(/\/$/, ""))) {
      deny(shellSyntax(word) ? "shell_metachar" : "git_form",
        `git add argument ${JSON.stringify(word).slice(0, 120)} is not a plain relative path`);
    }
    const relative = canonicalTarget(word, workspace, "stage");
    if (gitMetadata(relative)) {
      deny("git_metadata", "this lane never stages git metadata (.git*)");
    }
    if (!within(policy.gitAdd, relative)) {
      deny("path_not_allowed",
        `git add of ${JSON.stringify(relative).slice(0, 200)} is outside this lane's allowlist`);
    }
  }
}

function checkGitCommit(policy, segment) {
  if (!policy.gitCommit) {
    deny("command_not_allowed", "this lane does not commit");
  }
  if (!COMMIT_COMMAND.test(segment)) {
    const core = segment.replace(/ \|\| echo "No changes"$/, "");
    deny(shellSyntax(core) ? "shell_metachar" : "commit_form",
      "this lane commits only with `git commit -m \"<plain message>\"`");
  }
}

function checkCurl(policy, command) {
  const forms = policy.curl.map((rule) => `curl -s "${rule.prefix}<query>"`).join(" or ");
  if (!policy.curl.length) {
    deny("command_not_allowed", "this lane does not run curl");
  }
  const curl = CURL_COMMAND.exec(command);
  if (curl) {
    const url = curl[1];
    const rule = policy.curl.find((candidate) => url.startsWith(candidate.prefix));
    if (!rule) {
      deny("curl_url", `curl is limited to ${forms}`);
    }
    if (!URL_QUERY.test(url.slice(rule.prefix.length))) {
      deny("curl_query", `the curl query may use only letters, digits and _=&+:.%,()/@-; ${forms}`);
    }
    return;
  }
  const flags = /^curl((?: -[A-Za-z-]+)*) /.exec(command);
  if (shellSyntax(command)) {
    deny("shell_metachar", `no pipes, redirects or other shell syntax: run ${forms} alone `
      + "and read its output");
  }
  if (!flags || flags[1] !== " -s") {
    deny("curl_flag", `curl takes only -s (no -L or other flags): ${forms}`);
  }
  deny("curl_form", `curl takes one double-quoted URL with nothing after it: ${forms}`);
}

function checkUv(policy, command) {
  const forms = policy.uv.map((rule) => rule.base
    + (rule.suffix === ' "*' ? ' "<text>"' : rule.suffix)).join("; ");
  if (!policy.uv.length) {
    deny("command_not_allowed", "this lane does not run uv");
  }
  const ok = policy.uv.some((rule) => {
    if (rule.suffix === ' "*') {
      const opening = `${rule.base} "`;
      return command.length > opening.length + 1 && command.startsWith(opening)
        && command.endsWith('"') && UV_ARGUMENT.test(command.slice(opening.length, -1));
    }
    return command === rule.base + rule.suffix;
  });
  if (!ok) {
    const quoted = policy.uv.some((rule) => rule.suffix === ' "*'
      && command.startsWith(`${rule.base} "`));
    deny(shellSyntax(command) ? "shell_metachar" : quoted ? "uv_argument" : "uv_form",
      `uv is limited to: ${forms} (one double-quoted argument of letters, digits, spaces `
        + "and ._,:()/+'- where shown, nothing else)");
  }
}

function checkBash(policy, input, workspace) {
  if (!policy.gitAdd.length && !policy.gitCommit && !policy.curl.length && !policy.uv.length) {
    deny("tool_not_allowed", "tool \"Bash\" is not allowed in this lane");
  }
  const { command } = input;
  if (typeof command !== "string" || command === "" || command.length > 8192
    || /[\0\r\n\t]/.test(command)) {
    deny("shell_multiline", "the Bash command must be one plain line");
  }
  if (input.run_in_background === true) {
    deny("shell_background", "background Bash commands are not allowed in this lane");
  }
  if (command.startsWith("curl ")) {
    checkCurl(policy, command);
    return;
  }
  if (command.startsWith("uv ")) {
    checkUv(policy, command);
    return;
  }
  const parts = command.split(" && ");
  if (parts.length === 2 && parts[0].startsWith("git add ") && parts[1].startsWith("git commit ")) {
    checkGitAdd(policy, parts[0], workspace);
    checkGitCommit(policy, parts[1]);
  } else if (parts.length === 1 && command.startsWith("git add ")) {
    checkGitAdd(policy, command, workspace);
  } else if (parts.length === 1 && command.startsWith("git commit ")) {
    checkGitCommit(policy, command);
  } else {
    deny(shellSyntax(command) ? "shell_metachar"
      : command.startsWith("git ") ? "git_form" : "command_not_allowed",
    "this lane allows only `git add <its paths>`, `git commit -m \"<message>\"`, "
      + "their `&&` pair, its fixed curl URL, and its named uv scripts; use Read for "
      + "files and Glob for listings");
  }
}

function main() {
  const [settingsPath, workspaceArg, denialLogArg] = process.argv.slice(2);
  denialLog = denialLogArg ?? null;

  let raw;
  try {
    raw = readFileSync(0);
  } catch {
    deny("input_invalid", "the hook input is unreadable");
  }
  if (raw.length > MAX_INPUT_BYTES) {
    deny("input_invalid", "the hook input is too large");
  }
  let event;
  try {
    event = JSON.parse(raw.toString("utf8"));
  } catch {
    deny("input_invalid", "the hook input is not JSON");
  }
  const tool = event?.tool_name;
  toolName = typeof tool === "string" ? tool : null;
  const input = event?.tool_input;
  if (!input || typeof input !== "object") {
    deny("input_invalid", "the tool call has no input object");
  }
  const policy = loadPolicy(settingsPath);
  const workspace = canonicalWorkspace(workspaceArg);
  // Edit is absent on purpose: it compares old_string with the file before
  // any hook runs. Every other tool name falls through to the refusal.
  if (tool === "Read") {
    const relative = canonicalTarget(input.file_path, workspace, "read");
    if (!fileAllowed(policy, "Read", relative)) {
      deny("path_not_allowed",
        `Read of ${JSON.stringify(relative).slice(0, 200)} is outside this lane's allowlist`);
    }
  } else if (tool === "Write") {
    const relative = canonicalTarget(input.file_path, workspace, "write");
    if (gitMetadata(relative)) {
      deny("git_metadata", "this lane never writes git metadata (.git*)");
    }
    if (!fileAllowed(policy, "Edit", relative)) {
      deny("path_not_allowed",
        `Write of ${JSON.stringify(relative).slice(0, 200)} is outside this lane's allowlist`);
    }
  } else if (tool === "Glob") {
    checkGlob(policy, input, workspace);
  } else if (tool === "Bash") {
    checkBash(policy, input, workspace);
  } else {
    deny("tool_not_allowed",
      `tool ${JSON.stringify(String(tool)).slice(0, 80)} is not allowed in this lane`);
  }
  process.exit(0);
}

main();

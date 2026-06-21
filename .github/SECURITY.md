# Security Policy

## Reporting a vulnerability

Please **do not** open a public issue for security problems.

Use GitHub's private vulnerability reporting instead:
**Security** tab → **Report a vulnerability** (GitHub Security Advisories).
This opens a private channel with the maintainer.

Please include enough detail to reproduce (affected file/workflow, steps, and
impact). You can expect an initial acknowledgement within a few days.

## Scope

This project handles a few classes of sensitive material; reports touching
these are especially welcome:

- **Credentials** — the pipeline uses X/Twitter session cookies
  (`BIRD_AUTH_TOKEN`, `BIRD_CT0`) and several API keys, all injected via GitHub
  Actions secrets. They must never appear in the repo, logs, or `research/`
  output. See `.env.example` for the full list.
- **Workflow injection** — GitHub Actions workflows that consume
  attacker-influenced input (issue/PR titles and bodies) must route it through
  `env:` rather than interpolating it into `run:` blocks. Reports of unsafe
  interpolation are in scope.
- **Dashboard** — the SPA renders generated Markdown/HTML; it runs DOMPurify at
  runtime and the static SEO postbuild strips executable tags. XSS or sanitizer
  bypasses are in scope.

## Out of scope

- The contents of `research/` are automated reproductions of public
  third-party material; copyright/takedown concerns for a specific source
  should go to a regular issue, not the security channel.
- The default `https://*.guzus.xyz` service endpoints belong to the
  maintainer's deployment; testing against them is not authorized.

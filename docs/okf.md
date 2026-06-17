# Open Knowledge Format for ARA

ARA adopts the Open Knowledge Format (OKF) for portable knowledge sharing from
the persistent wiki at `research/wiki/`.

OKF v0.1 is an open Google Cloud specification for representing knowledge as a
directory of Markdown files with YAML frontmatter. See Google's introduction:
<https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing>
and the draft spec:
<https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md>.
Its core interoperability surface is deliberately small: each concept is one
Markdown file, the frontmatter has a required `type` field, and recommended
fields such as `title`, `description`, `resource`, `tags`, and `timestamp` make
the bundle easy for humans, agents, search indexes, and graph viewers to
consume.

ARA already has the same underlying mechanics: a git-versioned wiki of
interlinked Markdown pages with strict frontmatter and a generated dashboard
index. The maintained wiki pages now use OKF-native frontmatter fields at the
source, with a few ARA extension fields where the pipeline needs stricter local
behavior.

## Source Bundle

The source of truth remains:

```
research/wiki/
├── index.md
├── log.md
├── entities/
├── concepts/
└── themes/
```

Every non-reserved page under `entities/`, `concepts/`, and `themes/` is an OKF
concept document. `index.md` and `log.md` remain reserved navigation/history
files.

The ARA wiki is stricter than baseline OKF:

- It has exactly three canonical concept types: `entity`, `concept`, `theme`.
- Every page carries stable `slug`, `title`, `description`, `created_at`, and
  `timestamp` fields.
- Pages may carry an `images` gallery of visual depictions for the
  topic/description; this is preserved as an ARA extension field.
- Internal links use ARA wikilinks (`[[slug]]`, `[[slug|Label]]`) so the
  validator can resolve aliases and catch missing pages before publishing.
- `scripts/check_wiki.py` remains the source validator for the maintained wiki.

## OKF Export

Generate a portable OKF bundle from the maintained wiki:

```bash
uv run python scripts/export_wiki_okf.py --out /tmp/ara-okf
```

The exporter validates the wiki first, then writes a clean bundle containing:

- `index.md` — OKF-style bundle index grouped by entity, concept, and theme.
- `entities/*.md`, `concepts/*.md`, `themes/*.md` — one OKF concept document per
  wiki page.

The generated bundle is intended for sharing with agents and external tools.
It is not committed by default because `research/wiki/` is the canonical source
and the export is deterministic from that source.

## Field Mapping

| ARA wiki field | OKF export field | Notes |
|---|---|---|
| `type` | `type` | Preserved as `entity`, `concept`, or `theme`; OKF consumers must tolerate unknown producer-defined types. |
| `title` | `title` | Preserved unchanged. |
| `description` | `description` | OKF's one-line preview field. |
| `tags` | `tags` | Preserved unchanged. |
| `timestamp` | `timestamp` | Preserved as the OKF last-meaningful-change timestamp. |
| `slug` | `ara_slug` | Preserved as an ARA extension field. |
| `aliases` | `aliases` | Preserved as an extension field for agent lookup. |
| `created_at` | `created_at` | Preserved as an extension field. |
| `sources` | `sources` | Preserved as an extension field. |
| `images` | `images` | Preserved as an extension field. Each item has `url`, `alt`, and optional `caption`, `credit`, `source_url`. |

ARA does not force `resource` on wiki pages because many pages describe abstract
entities, concepts, or themes rather than a single underlying data asset.

## Link Mapping

ARA source pages use `[[wikilinks]]` because the local validator resolves slugs
and aliases. OKF consumers expect normal Markdown links, so the exporter rewrites
resolved wikilinks:

```markdown
[[openai]]              -> [OpenAI](../entities/openai.md)
[[openai|OpenAI lab]]   -> [OpenAI lab](../entities/openai.md)
[[An Alias]]            -> [Canonical Title](../entities/openai.md)
```

Unresolved wikilinks cannot reach the exporter because `scripts/check_wiki.py`
rejects them first.

## Compatibility Boundary

Baseline OKF consumers must tolerate ARA extension fields. ARA consumers should
not assume every OKF bundle has ARA fields such as `ara_slug`, `aliases`, or
`sources`; those are local affordances layered on top of the open format.

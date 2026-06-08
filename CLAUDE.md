# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> **Built from the EU legislative-tracker template.** The file this repo follows is defined once in
> [`tracker.yaml`](tracker.yaml); the `<PLACEHOLDER>` tokens below are filled from it by
> `python3 bootstrap.py`. Starting a fresh file? Read `SETUP.md` first.

## What this repo is

A personal, open **legislative tracker** — not a software project. It follows one EU file:
**<FILE-ID>**, the Commission's *<SHORT-NAME>* proposal **<PROPOSAL-ID> final** (<PROPOSAL-DATE>)
on the strand: <STRAND>. (These facts come from [`tracker.yaml`](tracker.yaml).)

**Scope guard:** this repo tracks `<FILE-ID>` **only**. It is *not* `<KEEP-APART-ID>`
(<KEEP-APART-NOTE>) — a separate file. Keep them apart. The authoritative scope is
[`tracker.yaml`](tracker.yaml) (`file_id` vs `keep_apart`).

There is no build, no app, no test suite. The "code" is Markdown + YAML + three Python skill drivers.

## Three-layer architecture (the big picture)

The repo deliberately separates three layers so links stay stable as the file evolves:

| Layer | Folder | What it is | Mutability |
|---|---|---|---|
| **Primary sources** | `sources/` | Register of every official document; PDFs/DOCX committed (incl. LIMITE — see `NOTICE` §2) | append-only |
| **Operative-text extracts** | `extracts/` | Diffable plain-text transcriptions of the operative articles, one set per version | versioned |
| **Analysis** | `docs/` | Human-readable analysis linking *down* into the two layers above | living |

`extracts/commission/` is the **base text** (the Commission proposal — the diff baseline).
`extracts/council/` holds one file-set **per Council compromise version** (`ST-<nnnn>-<yyyy>`),
structured identically so `git diff` between versions is meaningful. The slices in each set are listed
in [`tracker.yaml`](tracker.yaml) (`extract_slices`) — for this file: `_gdpr-art3-amendments`,
`_eprivacy-art5`, `_cyber-art6-9`, `_final-art10-11`, `_recitals` (plus informational cross-ref slices).
The shipped EXAMPLE set is the Commission baseline + Council `ST-9547-2026`.

## Single sources of truth (don't hand-edit downstream copies)

- **`data/documents.yaml`** is the canonical document register. `sources/README.md` is its *rendered*
  table — edit the YAML, then update the table to match. Never edit the table alone.
- **`data/tracker-state.yaml`** is **auto-maintained by the daily tracker routine** (a scheduled remote
  agent that hashes watched source pages T1-*/T2-*/T3-*). The header says "Do not edit by hand" — respect it.
- **`data/positions.csv`** backs the institutional/provision comparison; keep it in sync with the
  `docs/provisions/*` and `docs/institutional-positions.md` prose.
- **`STATUS.md`** is the one-screen current snapshot (format spec: `docs/reporting-standard.md`);
  **`TIMELINE.md`** is the full sourced chronology. `STATUS.md`'s "What changed" table (headline subset) and
  its full counterpart **`docs/what-changed.md`** (every tracked provision, deep-linked to the operative
  extracts) are the authority on what moved vs earlier reporting — consult them before asserting a feature
  of the proposal (features are routinely deleted/moved between compromise versions).

## Adding a Council compromise text (the core workflow)

When asked to transcribe / add a new ST compromise version, **use the `transcribe-council-extract` skill**.
The canonical faithfulness rules live in `extracts/council/_TRANSCRIPTION_GUIDE.md` — read it first;
`extracts/commission/_TRANSCRIPTION_GUIDE.md` adapts them for the base text.

Why this is non-trivial: the PDFs carry tracked changes (~~strikethrough~~ = deletion, **bold** = addition).
Plain `pdftotext`/`get_text()` **destroys that formatting** and merges old+new tokens (e.g. `9672 hours`
for "~~72~~ **96** hours"), silently producing *wrong legal text*. The skill's `pdf_changes.py` recovers
the markup from the PDF's structure; `render_pdf.py` page images are the cross-check (esp. for inline
single-number/short-word swaps, which `pdf_changes.py` can flip). Both must agree before committing.

Driver commands (run from repo root; `pip install pymupdf cffi` first — `cffi` is required):

```bash
# 1. Map every change (DELETED/NEW/AMENDED) before writing — the guardrail
python3 .claude/skills/transcribe-council-extract/pdf_changes.py "<source.pdf>" --all --mode summary
# 2. Extract consolidated + marked text to transcribe from
python3 .claude/skills/transcribe-council-extract/pdf_changes.py "<source.pdf>" --pages 2-16 --mode both
# 3. Visual cross-check (read the /tmp/*.png with the Read tool; start with the cover page)
python3 .claude/skills/transcribe-council-extract/render_pdf.py "<source.pdf>" --pages 1,18,19
# 4. Internal link + #anchor check (must end "0 broken") — mirrors the lychee CI
python3 .claude/skills/transcribe-council-extract/linkcheck.py .
```

Transcribe the **consolidated** result (changes applied, markup not reproduced), using the document's
**own** article/recital numbering (numbering shifts between versions — never copy a later version's numbers
onto an earlier text). Mark whole-provision deletions `[DELETED in ST <nnnn>/26]`, undecided source
brackets `[...]` preserved as-is, illegible passages `[illegible in source]`. Then branch
`extracts/st-<nnnn>-<yyyy>`, commit the file-set (not the `/tmp` PNGs), and PR to `main`.

## Conventions

- **Relative links only** inside the repo — never `github.com/...` absolute URLs (they break on rename/fork/mirror).
- **Deep-link into `extracts/*.md#anchor`, not `sources/*.pdf#page`** — GitHub's PDF viewer can't anchor to a page.
- **Document naming:** `<INSTITUTIONAL-ID>_<short-description>_<ISO-date>.<ext>` — stable number first, ISO
  date last, so chronological sort works (e.g. `ST-9547-2026_council-presidency-compromise_2026-05-21.pdf`).
- **Link checking (CI):** `lychee` runs on push/PR/weekly via `.github/workflows/link-check.yml`, configured
  by `lychee.toml`. Internal links are checked strictly; some external hosts (consilium register, EUR-Lex,
  Oeil, LinkedIn) are excluded because they bot-block or 404 for unreleased LIMITE docs.

## Disclaimer

Personal project, **not legal advice**, not any employer's view (`DISCLAIMER.md`). Original commentary is
CC BY 4.0 (`LICENSE`); EU documents and third-party works are not (`NOTICE`). Extracts are working
transcriptions — verify against the authoritative source before relying on them.

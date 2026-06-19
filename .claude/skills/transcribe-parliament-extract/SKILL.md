---
name: transcribe-parliament-extract
description: >-
  Transcribe a European Parliament committee text on the EU file this repo tracks
  (see tracker.yaml) — a draft opinion, draft report, tabled amendments, or adopted
  opinion/report — into the repo's structured markdown extracts under
  extracts/parliament/. Use when asked to transcribe / create an extract for an EP
  committee document (the lead/opinion committees listed in tracker.yaml
  co_legislators.parliament), add per-amendment operative text, or diff one committee
  version against another. Covers the EP two-column amendment-table format and link-checking.
---

# Transcribe an EP committee text into extracts

This repo stores each European Parliament committee text on the file it tracks
(see [`tracker.yaml`](../../../tracker.yaml): `file_id`) as a faithful, **diffable** markdown
transcription under `extracts/parliament/`, **one file per committee document**. The canonical rules
are in [`extracts/parliament/_TRANSCRIPTION_GUIDE.md`](../../../extracts/parliament/_TRANSCRIPTION_GUIDE.md) —
read it first; this skill is the *operational* companion.

**How this differs from `transcribe-council-extract`.** Council compromise texts are a single
**consolidated** redraft with tracked changes (strikethrough/bold), so that skill leans on
`pdf_changes.py` to recover the redline. EP committee texts are the opposite: a numbered list of
**discrete amendments**, each a clean two-column "Text proposed by the Commission | Amendment" table,
usually with a per-amendment *Justification*. There is **no redline to recover** — so
**`pdf_changes.py` does not apply here.** Transcribe each amendment as tabled, in the document's own
numbering; do **not** consolidate.

This skill **reuses the link-checker** from `transcribe-council-extract` — do not duplicate it:
- `linkcheck.py` — internal relative-link + `#anchor` check (the CI gate).

All paths below are relative to the **repo root**.

## The doceo bot-block (read before you fetch)

EP committee documents live on `www.europarl.europa.eu/doceo/...`. That host returns **HTTP 202 with
an AWS-WAF JS/CAPTCHA challenge** to every non-browser client — `curl` (any User-Agent) and WebFetch
get **0 bytes**, for both the `.pdf` and the `.docx`. A plain `curl`/WebFetch **cannot** fetch the operative text server-side — but the shared fetcher (below) drives a headless browser that does. Obtain the file one of these ways, then commit it under `sources/parliament/`:
1. **The shared fetcher** (preferred — solves the WAF for you):
   `python3 $HOME/law-tracker/lib/fetch_blocked_doc.py "<doceo-url>" "sources/parliament/<DOC-ID>_<slug>_<date>.pdf"`
   It tiers curl-impersonate → headless Chromium (doceo needs the browser tier, which it launches for you). Exit 0 → a validated PDF/DOCX is on disk, proceed. Exit 2/4 → unretrievable, or the fetcher is not set up (`~/law-tracker/lib/SETUP.md`); then fall back to a manual **browser download**.
2. A **non-WAF mirror** (occasionally EUR-Lex once adopted, or a national-parliament relay). The
   committee *documents* listing pages and OEIL confirm a document's existence + metadata even when the
   PDF body is unreadable — use them to verify, not to transcribe.

If you have only the cover page / a secondary lead (e.g. a Bluesky screenshot or a journalist's post)
and **not** the operative text: **do not create an extract.** Register metadata only and set
`pending_operative_text: true` (see `register-document` and `resolve-tracker-issue`), so the tracker
re-surfaces it.

## Reading the PDF — the Read tool is the primary path

The committed PDF is read with **Claude Code's Read tool**, which renders the PDF pages directly. This
is the workflow in practice:

1. Confirm the committed source exists: `ls sources/parliament/`. If it is not there, obtain it
   (above) and register it with `register-document` first.
2. **Read the cover page** (Read tool on the committed PDF, page 1–2) to fix metadata: committee,
   document number (e.g. PE-number), rapporteur, date, the interinstitutional file (must match this
   repo's `file_id` from `tracker.yaml` — guard against a `keep_apart` sibling file), and which lead
   committee it feeds.
3. **Read the amendment pages** (Read tool) and transcribe each amendment's two-column table faithfully
   (Commission text + Amendment), plus its target reference and *Justification*.
4. **Read the matching `../commission/` (and `../council/`) anchors** for the same articles so you can
   cross-link and so the diff lines up.
5. Write `extracts/parliament/<DOC-ID>_<short-desc>.md` per the guide: header blockquote (committee +
   doc no. + rapporteur + date + the `file_id` + lead committee + "working transcription, not an
   official text" + link to `../../NOTICE`); the document's **own** amendment numbering; explicit
   `<a id="amendment-N"></a>` HTML anchors (**not** `{#...}` suffixes — GitHub and the link-checker
   ignore those) plus per-provision anchors; `[...]`/`[illegible in source]` markers; cross-links to
   `../commission/`, `docs/provisions/*`, `docs/instruments/*`.
6. **Cascade** (or hand back to `resolve-tracker-issue`'s `parliament-text` playbook): update each
   touched `docs/provisions/*.md` Parliament section (or `docs/instruments/*.md`) and the `parliament`
   cell in `data/positions.csv` (deep-link the new amendment anchor), `docs/institutional-positions.md`,
   and `STATUS.md`/`docs/what-changed.md` if a tracked outcome moved. Clear `pending_operative_text` on
   the document entry.
7. **Link-check** (must end `0 broken`; fix link paths, never legal text):
   ```bash
   python3 .claude/skills/transcribe-council-extract/linkcheck.py .
   ```
8. Branch `extracts/<doc-id>`, commit the extract + cascade edits, push, open a PR to `main`.

> **Optional cross-check (`render_pdf.py`), only if pymupdf is available.** If the host has `pymupdf`
> (`fitz`) you may render page images as a visual cross-check:
> `python3 .claude/skills/transcribe-council-extract/render_pdf.py "<source.pdf>" --pages 1,2`
> then Read the `/tmp/*.png`. On a host with no pip / no pymupdf this will not run — the Read-tool path
> above is sufficient and is the primary method. Do **not** commit the `/tmp` PNGs.

## Run — human path
A human reads the committed PDF in a viewer and writes the markdown by hand; the Read/cross-check +
link-check steps still gate the result.

## Gotchas
- **Wrong file trap (scope).** A committee may issue an opinion on *both* sibling omnibus/package
  files. Confirm the cover's interinstitutional reference is **this repo's `file_id`** (`tracker.yaml`),
  not a `keep_apart` sibling. Verify the **rapporteur** too — the same committee can have *different*
  rapporteurs on the two sibling files, so a listing-page metadata summary can mis-attribute a row; the
  cover page is the tie-breaker. (EXAMPLE: for 2025/0360 confirm `2025/0360(COD)`, not the AI file
  `2025/0359(COD)`.)
- **A draft opinion is not a draft report.** A committee-for-opinion text feeds the lead committee's
  report; do not record it as the lead committee's draft report.
- **Secondary leads are not the text.** A Bluesky/LinkedIn/press summary is a lead for *which
  provisions* to expect — never a basis for verbatim amendment text.
- **`pdf_changes.py` is for Council redlines, not EP amendment tables** — using it here will mis-read
  clean two-column tables. Use the Read tool.

## Files used by this skill
- `../transcribe-council-extract/linkcheck.py` — internal link + `#anchor` checker (the CI gate).
- `../transcribe-council-extract/render_pdf.py` — optional page-image cross-check, only if pymupdf is
  installed.
(There is intentionally no `pdf_changes.py` step — see above.)

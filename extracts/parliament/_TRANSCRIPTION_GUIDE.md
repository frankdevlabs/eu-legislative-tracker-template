# Transcription guide for European Parliament committee-text extracts

Internal standard for every file in `extracts/parliament/`. The goal: each EP committee text
(draft opinion, draft report, tabled amendments, adopted opinion/report) is a faithful, diffable
transcription of its **operative amendments**, structured so cross-links from `../../docs/provisions/*`
and `../../docs/instruments/*` resolve and so successive versions diff meaningfully.

## What lives here (and how it differs from `../council/`)

Council compromise texts are a **consolidated** redraft of the whole operative text (changes against
the Commission proposal applied). **EP committee texts are not** — they are a numbered list of
**discrete amendments**, each in a two-column "Text proposed by the Commission | Amendment" table,
often followed by a per-amendment *Justification*. So:

- Do **not** consolidate. Transcribe the amendments **as tabled**, in the document's own order and
  numbering.
- The `transcribe-council-extract` skill's `pdf_changes.py` (which recovers strikethrough/bold tracked
  changes) **does not apply** here — EP amendment PDFs are clean two-column tables, not tracked-change
  redlines. Use the Read tool (below) to read the tables and `linkcheck.py` to validate links
  (it lives under `../../.claude/skills/transcribe-council-extract/`).

## Source of truth
The committed PDF/DOCX under `../../sources/parliament/` for that document. Transcribe from the file
on disk. Never transcribe from memory, a journalist's summary, or a Bluesky/screenshot lead — those
are leads only. **doceo bot-block:** `www.europarl.europa.eu/doceo/...` returns HTTP 202 with an
AWS-WAF JS challenge to all non-browser clients (PDF *and* DOCX), so `curl`/WebFetch cannot fetch it.
Obtain the file via a real browser download (which solves the challenge) or a non-WAF mirror, commit
it to `sources/parliament/`, then transcribe.

## How to read the PDF (primary: the Read tool)
The **primary** transcription method is to **Read the committed PDF directly with Claude Code's Read
tool** — it renders the PDF pages, so the two-column amendment tables, the target references, and the
*Justification* blocks are legible without any extra tooling. Read the cover page first to fix
metadata, then the amendment pages. This is the method used in practice.

> **No-pip / no-pymupdf caveat.** The `render_pdf.py` driver (page-image cross-check) needs `pymupdf`
> (`fitz`), which is often unavailable on the host. Treat it as an **optional cross-check only, if
> pymupdf is available** — not the main path. The Read-tool path above does not need it.

## Faithfulness rules (hard)
- Transcribe the operative wording of each amendment **verbatim**. This is primary legal text, not
  prose to paraphrase. Keep the Commission-text column too where it aids the diff (or note "Commission
  text: see `../commission/<base-file>.md#<anchor>`").
- Preserve the document's **own** amendment numbering and its target references exactly — e.g.
  *"Amendment 7 — Article 1 – paragraph 1 – point 3 — Regulation (EU) <number>, Article 4(1)"*.
- Transcribe the committee/rapporteur **Justification** under each amendment if present (it is the
  recorded reason and feeds the provision's Parliament section).
- Bracketed placeholders / undecided source brackets `[...]` preserved as-is; illegible passages
  marked `[illegible in source]` — never guess.
- Make **no claim the document does not support.** If only the cover page is confirmed (e.g. text not
  yet retrieved), do not create an extract — register metadata only and set `pending_operative_text`
  (see `register-document` / `resolve-tracker-issue`).

## Structure & anchors
- **One file per committee document**, named `<DOC-ID>_<short-desc>.md` to match `data/documents.yaml`
  and the repo convention — e.g. `<CMTE>-PA-<number>_draft-opinion.md`, `<CMTE>-AM-<number>_amendments.md`,
  `<CMTE1>-<CMTE2>-PR-<number>_draft-report.md`. (EP committee texts are per-committee documents, not
  the per-slice split used for Council consolidated texts.)
- Give every amendment a stable **explicit HTML anchor** `<a id="amendment-N"></a>`, and add a second
  anchor keyed to the affected provision where useful (e.g. `<a id="<instrument>-art4"></a>`) so
  `docs/provisions/*` / `docs/instruments/*` can deep-link to the exact amendment.
- **Use explicit `<a id="..."></a>` HTML anchors, NOT `{#...}` heading suffixes.** GitHub and the
  repo link-checker do **not** honour `{#...}` — a `#anchor` link to a `{#...}` suffix will fail the
  link check. Put the explicit `<a id="...">` on its own line just above the heading it labels.
- Group amendments by the instrument/article they touch where the document does, so the file reads in
  the same order as the provisions it feeds.

## Header block (every file)
Open with the same blockquote style as the Council/Commission files: source = committee + document
number + rapporteur + date + the interinstitutional file (the `file_id` in `tracker.yaml`) + the lead
committee it feeds + "working transcription, not an official text" + "verify against the authoritative
document (doceo / `<DOC-ID>_EN.pdf`)" + "See `../../NOTICE`."

> EXAMPLE header source line: **JURI draft opinion PE789.142v01-00, rapporteur <name>, 5 Jun 2026,
> file 2025/0360 (COD), feeding the joint ITRE/LIBE report** — one illustrative example only; use the
> committees and rapporteur for the file this repo tracks (see `tracker.yaml`
> `co_legislators.parliament`).

## Cross-links
Relative links only. Link the matching `../commission/` (and `../council/`) anchors for the same
article, and the relevant `../../docs/provisions/*` / `../../docs/instruments/*` pages. Verify every
internal link/anchor resolves
(`python3 ../../.claude/skills/transcribe-council-extract/linkcheck.py ../..`) before finishing.

---
name: transcribe-council-extract
description: >-
  Transcribe an EU Council compromise PDF (the file this repo tracks — see
  tracker.yaml) into the repo's structured markdown extracts. Use when asked to transcribe / create
  extracts for a new ST document, add a new compromise-text version under
  extracts/council/, produce consolidated operative text, or diff one Council
  version against another. Covers extracting tracked changes (strikethrough /
  bold) into consolidated text, cross-checking via page images, and link-checking.
---

# Transcribe a Council compromise text into extracts

This repo stores each Council compromise version of the file it tracks
(see [`tracker.yaml`](../../../tracker.yaml): `file_id`) as a faithful, **diffable** markdown
transcription under `extracts/council/`, one file per slice (`tracker.yaml` `extract_slices`). The canonical rules are
in [`extracts/council/_TRANSCRIPTION_GUIDE.md`](../../../extracts/council/_TRANSCRIPTION_GUIDE.md) —
read it first; this skill is the *operational* companion (how to actually pull
text off the PDF and verify the result).

**The one thing that makes this hard:** the PDFs show changes as tracked edits —
~~strikethrough~~ = deletion, **bold** = addition, **bold-underlined** = change
vs the Commission proposal. The guide wants the *consolidated* reading (changes
applied). Plain-text extraction **destroys that formatting** and interleaves
struck and added words (you get `9672 hours` for "~~72~~ **96** hours",
`datasubmitting` for "~~…their data~~ **submitting**…"), so transcribing from
`pdftotext`/`get_text()` silently produces *wrong legal text* — you cannot tell
a deleted recital from a retained one.

**`pdf_changes.py` recovers the formatting from the PDF's own structure** (bold
= font flag; struck = a thin vector line crossing a span's middle) and prints the
consolidated text with deletions removed. **This is the primary tool** — read its
output, not the raw text. `render_pdf.py` (page images) is the cross-check for
anything the markup gets wrong (see Gotchas). Both must agree before you commit.

All paths below are relative to the **repo root**.

## Prerequisites

```bash
pip install pymupdf cffi
```

`cffi` is required: without it `pypdf`/crypto backends fail with
`ModuleNotFoundError: No module named '_cffi_backend'`. PyMuPDF (`fitz`) does the
rendering.

## Run — agent path (this is the workflow)

1. Confirm the exact source filename:

   ```bash
   ls sources/council/
   ```

2. **Map every change first (`--mode summary`).** Get a one-line-per-item verdict
   (DELETED / NEW / AMENDED / unchanged) for the *whole* document before writing a
   word. This is the guardrail against the failure that prompted this tool: a whole
   recital that is struck through but still legible, mistaken for "retained":

   ```bash
   python3 .claude/skills/transcribe-council-extract/pdf_changes.py \
     "sources/council/ST-6406-2026_council-presidency-compromise_2026-02-20.pdf" --all --mode summary
   ```

   Most reliable on the **preamble** (every `(N)` is a recital). In the enacting
   articles `(N)` is also a definition/paragraph number, so those rows are noisy —
   treat them as hints. Keep this list; you reconcile against it in step 7.

3. **Extract the tracked changes.** `--mode both` prints the `~~deleted~~`/`**added**`
   markup, then the consolidated CLEAN text below a divider. Transcribe operative
   text from the CLEAN block; use the marked block to see *what* changed for `▸`:

   ```bash
   python3 .claude/skills/transcribe-council-extract/pdf_changes.py \
     "sources/council/ST-6406-2026_council-presidency-compromise_2026-02-20.pdf" --pages 2-16 --mode marked
   ```

   Whole-recital/whole-point deletions and additions are detected reliably (a
   recital shown entirely `~~struck~~` is `[DELETED]`; entirely `**bold**` is new).

4. **Cross-check with page images.** Render the cover and any clause the markup
   gets wrong (see Gotchas — esp. inline number/short-word swaps):

   ```bash
   python3 .claude/skills/transcribe-council-extract/render_pdf.py \
     "sources/council/ST-6406-2026_council-presidency-compromise_2026-02-20.pdf" --pages 1,18,19
   ```

   For a doubtful clause, a high-DPI vertical crop
   (`<page>:<y0frac>:<y1frac>[:dpi]`, repeatable):

   ```bash
   python3 .claude/skills/transcribe-council-extract/render_pdf.py \
     "sources/council/ST-6406-2026_council-presidency-compromise_2026-02-20.pdf" \
     --crop 21:0.27:0.40:340
   ```

   **Read the PNGs** (`/tmp/p01.png …`, crops `/tmp/pNN_<y0>-<y1>.png`) with the
   Read tool. Start with the **cover page** — it has the change legend, the subject
   line, the date, and the meeting (e.g. AGS = Antici Group (Simplification)). The
   cover's text layer is usually empty (image-only), so you *must* read its image.

5. Read the matching **reference version's** five files to mirror structure,
   `<a id="...">` anchors and header style, e.g.
   [`../../../extracts/council/ST-9547-2026_gdpr-art3-amendments.md`](../../../extracts/council/ST-9547-2026_gdpr-art3-amendments.md)
   and its siblings (`_eprivacy-art5.md`, `_cyber-art6-9.md`, `_final-art10-11.md`,
   `_recitals.md`).

6. Write the `extracts/council/ST-<nnnn>-<yyyy>_*.md` files (one per `tracker.yaml`
   `extract_slices`) per the guide: header blockquote (doc no. + LIMITE + date + meeting +
   the `file_id` from `tracker.yaml` + "working transcription, not an official text" + link to `../../NOTICE`);
   the document's **own** article/recital numbering; `▸` change-notes;
   `[DELETED in ST <nnnn>/26]`; `[illegible in source]`; sibling +
   `docs/provisions|instruments/*` cross-links. If a section is genuinely absent
   in this version, still create the file and state the absence + a one-line reason
   + cross-links.

7. **Reconcile against the status map.** Re-run `--mode summary` and check it
   item-by-item against what you wrote: every `DELETED` must be `[DELETED in ST …]`
   (or an absent point) in the extract, every `NEW` a newly-added item, every
   `AMENDED` reflected in the consolidated text + a `▸` note. Do the **whole**
   document — don't stop partway (the original miss was an unreviewed tail). Then
   verify links (must end with `0 broken`; fix only link paths, never legal text):

   ```bash
   python3 .claude/skills/transcribe-council-extract/linkcheck.py .
   ```

8. Branch `extracts/st-<nnnn>-<yyyy>`, commit the five files, push, open a PR to
   `main`. Do **not** commit the `/tmp` PNGs.

## Run — human path

There is no app. A human reads the PDF in a viewer and edits the markdown by
hand; the rendering + link-check steps above are still the reliable way to get
tracked-change-accurate text and to gate the result.

## Gotchas (battle scars)

- **A struck-through recital is still perfectly legible — and means DELETED.**
  This is the trap that prompted the tool: read by eye, a whole struck recital
  looks "retained"; it is the opposite. Always run `--mode summary` and reconcile
  every item (step 7). A missed strikethrough silently *inverts* the legal status.
- **Never transcribe from `pdftotext`/`page.get_text()` for operative text.** It
  drops strikethrough/bold and merges old+new tokens (`9672`, `datasubmitting`).
  Use `pdf_changes.py`; cross-check the image.
- **`pdf_changes.py` can FLIP an inline replacement where the new and old tokens
  overlap horizontally.** The strike line over the deleted token can also cross
  the added token's box, so a short swap like "~~72~~**96** hours" may print as
  "~~96~~**72**". Block-level add/delete (whole recitals, whole points) is
  reliable; **single numbers / short words that replace each other are the weak
  spot** — verify every such inline swap against a `--crop` image. (Real case this
  session: Art 33(1) is **96 hours** — 72 struck, 96 added — but the tool tagged it
  backwards; the image settled it.)
- **`MuPDF error: ... No common ancestor in structure tree`** on stderr is
  harmless — rendering still succeeds (the example commands `2>/dev/null` it).
- **Numbering shifts between versions.** Use the document's own point/article and
  recital numbers; never copy a later version's numbers onto an earlier text.
- **A version can omit whole sections.** E.g. ST 6406/26 (Feb) has *no* operative
  ePrivacy (Art 5) or cyber (Arts 6–9) articles and no Article 11 — only a
  *bracketed* `[via the single-entry point … Article 23a of Directive (EU)
  2022/2555]` hook inside GDPR Art 33. Create the file and document the absence.
- **Bracketed `[...]` / `[OP: insert date = ...]` are undecided in the source** —
  preserve the brackets in the transcription; that is *not* `[illegible]`.
- **Same legal point can move between an article and a recital across versions**
  (e.g. AI legitimate interest = operative Art 88c + recitals 30/31 in Feb, but
  only recital 33a in May). Note the move in a `▸` change-note and cross-link.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `ModuleNotFoundError: No module named '_cffi_backend'` | `pip install cffi` |
| `PyMuPDF missing` from the driver | `pip install pymupdf cffi` |
| Rendered PNG is blank / image-only | it's a scanned cover or wrong page — re-render that page, or `--crop` at higher dpi |
| `linkcheck.py` reports a missing anchor | the `#fragment` doesn't match any `<a id>` or heading slug in the target — fix the link, not the heading |
| lychee CI red but `linkcheck.py` green | an *external* host rate-limited; check the excludes in `lychee.toml` (CI tolerates 403/429) |

## Files in this skill

- `pdf_changes.py` — **primary.** Recover tracked changes from the PDF structure;
  `clean` (consolidated), `marked` (`~~del~~`/`**add**`), `both`, or `summary`
  (one-line per-item DELETED/NEW/AMENDED verdict for reconciliation).
- `render_pdf.py` — render full pages / zoom crops to `/tmp` for visual reading
  (the cross-check, and the only way to settle inline-overlap swaps).
- `linkcheck.py` — internal relative-link + `#anchor` checker over `**/*.md`
  (mirrors the scope of the repo's lychee CI so you can verify before pushing).

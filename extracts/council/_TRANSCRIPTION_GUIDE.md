# Transcription guide for Council compromise-text extracts

Internal standard for every file in `extracts/council/`. The goal: each version's extract is a
faithful, diffable transcription of that version's operative text, structured identically across
versions so `git diff` between them is meaningful.

## Source of truth
The committed PDF under `sources/council/` for that document. Transcribe from the PDF on disk.
Never transcribe from memory, a web summary, or another version's text.

## Consolidated reading
Each compromise text shows changes *against the Commission proposal* (additions bold/bold-underline,
deletions strikethrough). Transcribe the **consolidated** result — i.e. apply the changes and write
the resulting operative text — exactly as the May file (`ST-9547-2026_*`) does. Do NOT reproduce the
strikethrough/bold markup itself; render the resulting text.

## Faithfulness rules (hard)
- Transcribe operative wording verbatim from the PDF. This is primary legal text, not prose to
  paraphrase. Do not summarise an article and call it a transcription.
- If a passage is illegible/uncertain in the PDF, mark it `[illegible in source]` — never guess.
- Use the document's OWN article and recital numbering. Numbering shifted between versions
  (especially the post-Article-88 GDPR articles and all recital numbers). Do not copy the May
  numbering onto an earlier text.
- Where the version deletes a whole provision, mark it `[DELETED in ST <nnnn>/26]` with a one-line
  note, mirroring the May file's `[DELETED in ST 9547/26]` convention.
- Flag the salient change for each point with a `▸` change-note (what moved vs the Commission
  proposal and, where known, vs the previous compromise text).

## Structure & anchors
- Reuse the heading text and `<a id="...">` anchors from the matching May file so cross-links and
  diffs line up — BUT only for points that exist in this version. If a point exists here but not in
  May (or vice versa), keep its own heading and add an anchor following the same slug pattern
  (`point-N--article-X-topic`).
- Keep the same five-file split as the May text:
  `_gdpr-art3-amendments.md`, `_eprivacy-art5.md`, `_cyber-art6-9.md`, `_final-art10-11.md`,
  `_recitals.md`. If a version genuinely lacks a section, still create the file and state that the
  section is absent/unchanged in that version, with a one-line explanation.
- Recitals file: curated subset (the contested/structural ones), like the May file. State that it is
  a curated subset, not the full preamble.

## Header block (every file)
Open with the same blockquote style as the May files: source doc number + LIMITE + date + AGS meeting
it served + interinstitutional file 2025/0360 (COD) + "working transcription, not an official text" +
"verify against the authoritative document. See `../../NOTICE`."

## Cross-links
Relative links only. Link sibling extracts and the relevant `docs/provisions/*` / `docs/instruments/*`
pages where the May files do. Verify every internal link/anchor resolves before finishing.

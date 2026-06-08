# Transcription guide for Commission base-text extracts

Internal standard for every file in `extracts/commission/`. The goal: a faithful, diffable
transcription of the **operative text of the Commission proposal COM(2025) 837 final** (CELEX
52025PC0837), structured to line up with the Council extracts in `../council/` so that
`git diff --no-index ../commission/COM-2025-837_<strand>.md ../council/ST-<nnnn>-<yyyy>_<strand>.md`
is meaningful.

## Source of truth
The committed proposal under `../../sources/commission/COM-2025-837_proposal_2025-11-19.docx` (the
enacting articles and recitals), cross-checked against the authoritative EUR-Lex copy
(CELEX **52025PC0837**). The accompanying correlation-table annex is
`../../sources/commission/COM-2025-837_annex1-correlation-tables_2025-11-19.docx`. Transcribe from the
committed source on disk; never from memory or a web summary.

## This is the baseline — there are no tracked changes
Unlike the Council compromise texts, the Commission proposal is the **original**: there is nothing to
"consolidate". What the proposal *does* contain is its **own amending instructions** to each existing
instrument — *"In Article 4, point 1, the following sentences are added: …"*, *"Article 22(1) and (2)
are replaced by the following: …"*. Transcribe those instructions and the **inserted/replacement
operative text verbatim**, as the proposal presents them. Use a `▸` change-note to flag what the
proposal changes **versus the pre-existing instrument** (e.g. "new derogation", "replaces current
Art 22(2)"), and — where it helps the reader — what the **Council later did** to that point, linking to
the matching `../council/` anchor.

## Faithfulness rules (hard)
- Transcribe operative wording verbatim. This is primary legal text, not prose to paraphrase.
- Preserve the proposal's own numbering of amending points and of the inserted articles/paragraphs.
- Preserve bracketed placeholders exactly — e.g. `[OP: please insert the date = 6 months following …]`
  — that is *not* `[illegible]`; it is undecided in the source.
- If a passage is genuinely illegible/uncertain in the source, mark it `[illegible in source]` — never
  guess.

## Structure & anchors
- Reuse the heading text and `<a id="...">` anchors from the matching `../council/ST-9547-2026_*` file
  wherever a point corresponds, so cross-links and cross-version diffs line up. Where the proposal has a
  point the Council later deleted (e.g. GDPR Art 88a, 88c), keep it here with its own heading + an anchor
  following the same slug pattern (`point-N--article-X-topic`).
- File split mirrors the Council strands, by the proposal's **own** article numbering (which happens to
  align): `COM-2025-837_gdpr-art3-amendments.md` (Art 3), `_eprivacy-art5.md` (Art 5),
  `_cyber-art6-9.md` (Arts 6–9), `_final-art10-11.md` (Arts 10–11), `_recitals.md` (curated subset).
  For full coverage the proposal's other amending articles also get a file: `_dataact-art1.md` (Art 1),
  `_sdg-art2.md` (Art 2), `_eudpr-art4.md` (Art 4).
- Recitals file: curated subset (the contested/structural ones), like the Council file. State that it is
  a curated subset, not the full 60-recital preamble.

## Header block (every file)
Open with the same blockquote style as the Council files: source = **COM(2025) 837 final**, 19 Nov 2025,
interinstitutional file **2025/0360 (COD)**, "working transcription, not an official text", "verify
against the authoritative document (EUR-Lex CELEX 52025PC0837)", and "See `../../NOTICE`."

## Cross-links
Relative links only. Link the sibling extracts, the matching `../council/` anchors, and the relevant
`../../docs/provisions/*` / `../../docs/instruments/*` pages. Verify every internal link/anchor resolves
(`python3 ../../.claude/skills/transcribe-council-extract/linkcheck.py ../..`) before finishing.

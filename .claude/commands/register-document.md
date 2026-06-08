---
description: Register one new official document on the tracked file into the register (optionally a draft PR)
argument-hint: "<url-or-path> [--pr]"
---

Use the **register-document** skill to add a single new document for the file this repo tracks
(see `tracker.yaml`: `file_id`) to the repo's single source of truth. Arguments: `$ARGUMENTS`.

Rules:
- Register **exactly one** document per run. Never bundle several into one entry or PR (a document
  plus its own cover note/annex counts as one).
- If no URL or path is given, ask for one (or the document metadata) and stop.
- Follow the skill's workflow: gather metadata (WebFetch the URL and/or Read the PDF directly when its
  text won't extract), pick the `sources/<folder>` by `body` and commit the file with the
  `<ID>_<slug>_<ISO-date>.<ext>` convention, append the `data/documents.yaml` entry, render the
  `sources/README.md` row, then route the substance to `TIMELINE.md` / `STATUS.md` and the right
  `docs/` page (`docs/member-state-positions.md` for national positions, `docs/advisory/*` for
  EDPB-EDPS/ECB/EESC, `docs/stakeholders.md` for NGO/industry).
- A full Council compromise text → register here, then hand transcription to the
  **transcribe-council-extract** skill (do not transcribe operative text in this skill).
- Always run `python3 .claude/skills/transcribe-council-extract/linkcheck.py .` (must end "0 broken")
  before committing.
- Flag handling:
  - no flag → make the edits on a new `documents/<doc-id>` branch and leave them committed locally
    for review (no push).
  - `--pr` → also push the branch and open a **draft** PR.

Read `.claude/skills/register-document/SKILL.md` for the body→folder map, the YAML field reference,
the `access:` values and the worked NL example.

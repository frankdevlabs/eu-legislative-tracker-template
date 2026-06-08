---
description: Triage one flagged "[tracker]" GitHub issue into a focused plan (optionally a draft PR / applied fix)
argument-hint: "[issue-number] [--pr|--fix]"
---

Use the **resolve-tracker-issue** skill to handle a single tracker finding for the file this
repo tracks (see `tracker.yaml`: `file_id`). Arguments: `$ARGUMENTS`.

Rules:
- Operate on **exactly one** issue. Never bundle issues into one plan or PR.
- If no issue number is given, just run
  `python3 .claude/skills/resolve-tracker-issue/tracker_issues.py --list`
  and show the open, untriaged tracker issues so the user can pick one. Stop there.
- If an issue number is given, follow the skill's workflow: resolve it with
  `tracker_issues.py --issue <n>`, fetch and confirm the source, run the matching
  playbook, and write the plan to `docs/triage/<date>-issue-<n>.md`.
- Flag handling:
  - no flag → leave the plan in the working tree for review (no branch).
  - `--pr` → branch, commit the plan, push, open a **draft** PR, label the issue
    `plan-drafted`, comment the PR link.
  - `--fix` → as `--pr`, plus apply the playbook's downstream edits on the branch and
    run `python3 .claude/skills/transcribe-council-extract/linkcheck.py .` (must end
    "0 broken") before committing.

Read `.claude/skills/resolve-tracker-issue/SKILL.md` for the playbooks and the plan template.

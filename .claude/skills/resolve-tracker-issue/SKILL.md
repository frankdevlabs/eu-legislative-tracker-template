---
name: resolve-tracker-issue
description: >-
  Triage and integrate ONE flagged tracker finding for the EU file this repo tracks (see tracker.yaml).
  Use when asked to resolve / triage / action a "[tracker] ..." GitHub issue,
  integrate a flagged source change into the repo, draft a plan for what the
  daily tracker found, or work through the open tracker issues. Produces one
  focused plan per issue under docs/triage/ (optionally a draft PR, optionally
  applying the downstream edits) — never bundles issues together.
---

# resolve-tracker-issue

The daily tracker cron (`~/law-tracker/run.sh`, weekdays ~12:00 UTC) detects what
is new across the watched sources and opens **one GitHub issue per hit**, labelled
`tracker` + a tier (`tier-1/2/3`) + a topic. Those issues are the flagged
information someone must integrate into the repo's analysis layers. This skill
turns one such issue into a focused, executable plan — and, on request, applies it.

## The one rule

**Operate on exactly ONE issue per run and per plan file.** Never combine issues.
Each flag gets its own `docs/triage/<date>-issue-<n>.md` and its own branch/PR.
If asked to "do them all", loop the resolver once per issue — separate plan, separate PR each.

## Inputs and modes

The entry point is the `/tracker-issue` command (or invoke this skill directly).
`$ARGUMENTS` is an issue number plus an optional flag:

- **(no number)** → list open, untriaged tracker issues and stop:
  `python3 .claude/skills/resolve-tracker-issue/tracker_issues.py --list`
- **`<n>`** → produce the plan for issue `<n>` in the working tree; do not branch. (on-the-fly review)
- **`<n> --pr`** → also branch, commit the plan, push, open a **draft** PR, and mark the
  issue triaged. This is what the cron uses. Plan only — no downstream content edits.
- **`<n> --fix`** → implies `--pr`, and additionally applies the downstream edits per the
  playbook on the same branch, running the link check before committing.

## Workflow

1. **Resolve the issue.** Run the helper to get the parsed, watchlist-joined record:
   ```bash
   python3 .claude/skills/resolve-tracker-issue/tracker_issues.py --issue <n>
   ```
   This returns `type`, `playbook`, `codes`, `source_url`, `detected_at`, `why`,
   `excerpt`, `affects[]`, `document_id`, `watchlist_label`. The `affects` list is the
   set of downstream files to consider — it comes from the watchlist in `tracker.yaml`.

2. **Gather evidence.** Fetch `source_url` (WebFetch) and compare against what the repo
   already records. The issue `excerpt` is a lead, not ground truth — confirm against the
   live source and apply the **scope rule** from [`tracker.yaml`](../../../tracker.yaml):
   in-scope only if it concerns this repo's file (`file_id`), not a `keep_apart` sibling.
   (Watch foreign-language sources especially — check the file number, not just the topic.)
   If it is a `keep_apart` file or otherwise off-topic, the plan's recommendation is to
   **close the issue as not-relevant** — do not edit the repo.

3. **Run the matching playbook** (below) to determine the concrete edits.

4. **Write the plan** to `docs/triage/<date>-issue-<n>.md` using the template below.
   `<date>` is the issue's `detected_at` date (fallback: today, UTC).

5. **Per the mode:** stop (default), open a draft PR (`--pr`), or apply + PR (`--fix`).
   See "Opening the PR".

## Playbooks (by `playbook` field)

### `institutional` — Tier-1 procedural / advisory hit
Decide whether the change is **substantive** (a real procedural step or position) or
**noise** (rotating widget, transparency-meeting log, unchanged re-publish — common for
T1-05/06/07). If substantive:
- New procedural fact (committee referral, rapporteur, vote, meeting date) → update the
  relevant institution field (and **Next milestones**) in `STATUS.md` and add a sourced
  row to `TIMELINE.md`.
- New advisory output (EDPB/EDPS, ECB, EESC) → update the matching `docs/advisory/*.md`
  and `docs/institutional-positions.md`; register the document in `data/documents.yaml`
  (then regenerate the `sources/README.md` table) if it is a new committed document.
- Always check `STATUS.md`'s "What changed" table (full version: `docs/what-changed.md`) before asserting a
  feature of the proposal — several widely-reported features were deleted/moved.

### `council-text` — Tier-1 Council source (T1-08/T1-09), highest priority
A new ST LIMITE compromise text is the heaviest case:
- Register the document in `data/documents.yaml`; update `sources/README.md`.
- **Hand off transcription to the `transcribe-council-extract` skill** — do not transcribe
  by hand. Produce the extract set (one file per `tracker.yaml` `extract_slices`) under
  `extracts/council/ST-<nnnn>-<yyyy>...`.
- Cascade: update the affected `docs/provisions/*.md`, `docs/institutional-positions.md`,
  `data/positions.csv`, `STATUS.md` + the full `docs/what-changed.md` diff table, `TIMELINE.md`.
- Because this spans many files, a `--fix` run here is large; prefer producing the plan and
  letting a human drive the transcription, unless explicitly told to apply.

### `stakeholder-social` — Tier-2 NGO/media/law-firm or Tier-3 Bluesky
Judge whether the item is a substantive position/analysis or just commentary:
- Substantive → add/extend an entry in `docs/stakeholders.md` (and `docs/fault-lines.md`
  for noyb/EDRi positions; `docs/member-state-positions.md` for national-DPA / NL items),
  cross-linking the relevant `docs/provisions/*`.
- Pure commentary / off-topic → recommend closing the issue; no repo edit.

### `source-health` — the weekly `[tracker] Source health` issue (or a state-blocked issue)
Not a content change — a fetch problem. For each listed code:
- Check its `url` in `tracker.yaml` (`watchlist.sources`) and `data/documents.yaml`. Is it stale,
  moved, or just temporarily blocked (Cloudflare/AWS-WAF 403/202/503)?
- Propose: a corrected URL, a fallback endpoint, or marking the source unreachable.
  Defunct feed → propose removal/replacement in `tracker.yaml` and the cron
  prompt. This mirrors the earlier source-health PR pattern. The plan lists the per-source
  verdict; `--fix` edits `tracker.yaml`/`documents.yaml` accordingly.

### `run-summary` / `skip`
Suppressed-hits summary issues need no integration — the helper already filters them out.

## Plan file template

```markdown
# Triage: issue #<n> — <short title>

- **Issue:** <issue_url>
- **Source:** <watchlist_label> (`<code>`) — <source_url>
- **Detected:** <detected_at>
- **Type / playbook:** <type> / <playbook>

## What was flagged
<the `why`, plus the confirmed observation from fetching the source>

## Assessment
<substantive vs noise / in-scope vs AI-Act-only; the judgement and why>

## Plan
<numbered, concrete steps — exact files from `affects` and the edit each needs.
 If the recommendation is "close as not-relevant", say so and why.>

## Verification
<how to confirm: link check, the specific doc/section to read, gh issue close>
```

## Opening the PR (`--pr` / `--fix`)

```bash
date_tag="<detected_at date or today>"
git checkout -b "triage/${date_tag}-issue-<n>"
# (--fix only) apply the playbook edits here, then:
python3 .claude/skills/transcribe-council-extract/linkcheck.py .   # must end "0 broken"
git add docs/triage/${date_tag}-issue-<n>.md <any --fix edits>
git commit -m "triage: plan for #<n> (<code>)"
git push -u origin "triage/${date_tag}-issue-<n>"
gh label create plan-drafted --description "Tracker issue has a triage plan PR" --color ededed --force
gh pr create --draft --title "triage: #<n> <short title>" \
  --body "Resolves the integration plan for #<n>. See docs/triage/${date_tag}-issue-<n>.md.\n\nCloses #<n> once merged." 
gh issue edit <n> --add-label plan-drafted
gh issue comment <n> --body "Triage plan drafted: <PR link>."
```

All plan PRs share the single `docs/triage/` folder. The `plan-drafted` label is what makes
the cron loop and `--list` skip already-handled issues, so always apply it on `--pr`/`--fix`.

## Conventions (inherited from the repo)
- Relative links only inside the repo; deep-link to `extracts/*.md#anchor`, not PDF pages.
- The link check must pass ("0 broken") before any `--fix` commit.
- Personal tracker, not legal advice; extracts are working transcriptions — verify against source.

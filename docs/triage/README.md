# Triage plans

Per-issue working plans for integrating what the daily tracker flags.

The daily tracker cron opens one `[tracker] …` GitHub issue per hit (see
`data/watchlist.yaml` for what each source feeds). The
[`resolve-tracker-issue`](../../.claude/skills/resolve-tracker-issue/SKILL.md) skill —
run on the fly via `/tracker-issue <n>` or automatically after each cron run — turns one
such issue into a focused plan here.

- **One file per issue**, named `<detected-date>-issue-<n>.md`. Plans are never bundled.
- Each is a transient working document: the concrete steps to integrate (or to close as
  not-relevant) that single finding. Once its draft PR is merged and the change is in the
  analysis layers, the plan file can be deleted (it has served its purpose; the change
  itself lives in `STATUS.md` / `TIMELINE.md` / `docs/provisions/*` / `extracts/`).
- Not legal advice; see [`../../DISCLAIMER.md`](../../DISCLAIMER.md).

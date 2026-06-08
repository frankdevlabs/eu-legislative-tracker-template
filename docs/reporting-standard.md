# Reporting standard — the `STATUS.md` snapshot format

This is the governing spec for the one-screen status snapshot. It travels with every tracker repo in this
family (one EU file per repo). `STATUS.md` is the live instance for this file;
[`STATUS.template.md`](../STATUS.template.md) is the blank copy-target for a new tracker. Keep all three in
step — change the format here, then mirror it in the template and the live file.

The point of standardising is that any reader (or sibling tracker) sees the **same shape**: a dashboard, the
OLP actors in the same order with the same fields, a forward look, and a latest-text diff. Only the names,
dates and links differ between files.

## Fixed section order

1. `# Status snapshot — <FILE-ID>` + the **dashboard table** + the not-legal-advice blockquote
2. `## One-line status`
3. `## Where each institution stands` (the OLP actors)
4. `## Next milestones to watch`
5. `## What changed in the latest text vs earlier reporting` (optional; see below)

## Dashboard table (top of file)

Six rows, always: **Procedure** · **Proposal** · **Legal bases** · **OLP stage** · **Latest text** · **As of**.
It is the at-a-glance answer to "what is this and where is it"; everything below expands it.

## "Where each institution stands" — the OLP skeleton

One block per actor, in procedure order: the **proposer** (Commission), then each **co-legislator** (Council,
Parliament), then a combined **Advisory bodies & Member States** block. Mark each heading with its role
(`— proposer` / `— co-legislator`).

Every institution block uses the **same five fields, in this order**:

- **Stage** — where this actor is in the procedure (e.g. "working-party stage", "committee referral only").
- **Latest act** — the newest document or event for this actor, with links (see linking rule).
- **Owner** — who holds it: DG / Commissioner / Presidency / rapporteur(s).
- **Position** — one-line substantive stance; link down for detail.
- **Next** — this actor's next expected step.

**Advisory bodies & Member States** is a table instead of five fields: one row per advisory body
(`Body | Latest act (date) | Position`) and one summary row for Member States linking to
[`member-state-positions.md`](member-state-positions.md).

Link **down**; do not duplicate. The snapshot is the index layer: chronology lives in
[`TIMELINE.md`](../TIMELINE.md), provision-by-provision positions in [`positions.csv`](../data/positions.csv)
and [`docs/provisions/`](provisions/), opinion substance in [`docs/advisory/`](advisory/).

## "Next milestones to watch"

A `[ ]` checklist of forward-looking events, dated where possible. Flag any item sourced only via a national
parliament as "verify against the institution". **Keep this heading verbatim** — the skills route new
milestones to it by name.

## "What changed in the latest text vs earlier reporting"

The myth-buster: a table of provisions that moved between first reporting and the latest operative text, so
nobody asserts a deleted/moved feature. Keep the **heading generic** (`the latest text`) and name the
specific version in the intro line — this way the heading and every reference to it survive a new compromise
text. This table is the **authority on what moved**; it is referenced from [`CLAUDE.md`](../CLAUDE.md) and the
skills. Omit the whole section only while nothing has diverged from first reporting.

**Columns trace provenance, three lanes:** `Provision | Current law → Commission proposal | Latest
[co-legislator] text`. The point is to show *which institution changed what* — so always **state the
current-law baseline AND the proposal separately; never fold a status-quo figure into the "proposal" cell**
(e.g. GDPR's 72h breach deadline is *current law*, not the Commission's 96h proposal — getting this wrong is
the classic error this table exists to prevent).

**Two links per row (interactivity).** Link the **provision** cell to its [`docs/provisions/`](provisions/)
analysis page, and end each substantive cell with a deep link into the operative text — the Commission column
into [`extracts/commission/`](../extracts/commission/), the latest-text column into the matching
[`extracts/`](../extracts/) `#anchor` (prefer a stable explicit `<a id=…>` anchor over a heading slug).

**Lean summary + full detail.** When a file has many changed provisions, `STATUS.md` carries only a **headline
subset** (the high-salience / contested provisions) plus a pointer; the **full provision-by-provision table**
lives in [`docs/what-changed.md`](what-changed.md) (covering every row in [`positions.csv`](../data/positions.csv),
grouped by instrument). `what-changed.md` is then the comprehensive authority; the `STATUS.md` table is its
at-a-glance extract. Refresh **both** on a new compromise text.

## Linking convention

Every document or report named in the snapshot gets **two links**:

- **Internal** — a [`docs/`](.) digest or an [`extracts/`](../extracts/) anchor where one exists, otherwise
  the document's row in [`sources/README.md`](../sources/README.md). Never deep-link a raw `sources/*.pdf`
  (GitHub's PDF viewer can't anchor a page). Relative paths only — never `github.com/...` URLs.
- **External** — the authoritative URL, taken from [`data/documents.yaml`](../data/documents.yaml)
  (`url` / `celex` / `mirror` / `national_parliament`). `documents.yaml` is the single source of truth for
  these URLs; do not invent them.

CI (lychee) checks internal links strictly and excludes a few external hosts that bot-block or are cited by
number (see [`lychee.toml`](../lychee.toml)); `accept` already absorbs 403/429. Before adding a new external
host, confirm it returns an accepted code, else add it to the exclude list.

## "As of" convention

Set **As of** to the **date of `last_run`** in [`data/tracker-state.yaml`](../data/tracker-state.yaml) — the
day the daily tracker last checked the watched sources. This ties the human snapshot date to the machine
freshness signal. (Documented, not automated — the repo has no build step.)

## Routing map — where each update lands

| New information | Where it goes in `STATUS.md` | Also update |
|---|---|---|
| Procedural milestone (referral, vote, meeting, appointment) | the actor's **Latest act** / **Next** field; add a `[ ]` to **Next milestones** if forward-looking | a sourced row in [`TIMELINE.md`](../TIMELINE.md) |
| New advisory opinion (EDPB/EDPS, ECB, EESC, CoR…) | a row in the **Advisory bodies** table | a [`docs/advisory/`](advisory/) digest |
| Member-state signal (non-paper, delegation comments) | the **Member States** row | [`member-state-positions.md`](member-state-positions.md) |
| New Council compromise text | dashboard **Latest text** + Council **Latest act**; refresh the **What changed** headline table | the full [`docs/what-changed.md`](what-changed.md) table, [`positions.csv`](../data/positions.csv), [`extracts/council/`](../extracts/council/) |

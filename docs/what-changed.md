# What changed — full provision-by-provision diff

> **TEMPLATE.** This page is the comprehensive companion to `STATUS.md`'s "What changed"
> summary — the **authority on what moved**. For every tracked provision it traces
> **current law → Commission proposal → latest Council text**, so it is clear *which institution changed
> what*. The single EXAMPLE row below (from reference file 2025/0360) shows the format; add one row per
> provision in [`data/positions.csv`](../data/positions.csv), grouped by amended instrument
> ([`tracker.yaml`](../tracker.yaml) `instruments`).

Why this page exists: widely-reported "features of the proposal" are routinely deleted, moved or already
in the base text. This is the myth-buster. (Reference-file example: the **Art 33** 96-hour deadline and
high-risk-only threshold were already in the *Commission* proposal — the Council changed only the routing
and timeline, a distinction this table exists to preserve.)

**How to read each row.** The **provision** cell links to its analysis page in [`provisions/`](provisions/);
each substantive cell ends with a deep link into the operative text — the **Commission** column into
[`extracts/commission/`](../extracts/commission/), the **Council** column into
[`extracts/council/`](../extracts/council/). State the **current-law baseline AND the proposal separately**
(never fold a status-quo figure into the "proposal" cell). Working transcriptions — **verify against the
authoritative source**.

## <Instrument 1, e.g. GDPR (Regulation (EU) 2016/679)>

| Provision | Current law → Commission proposal | Latest Council text (ST <nnnn>/<yy>) |
|---|---|---|
| [**Breach notification (Art 33)**](provisions/gdpr-art33-breach-notification.md) | *Current GDPR:* notify the DPA within **72h** unless the breach is "unlikely to result in a risk". **The Commission already moves to 96h + a high-risk-only threshold**, routed through the EU single-entry point. [Commission pt 8](../extracts/commission/COM-2025-837_gdpr-art3-amendments.md#point-8--article-33-breach-notification) | **96h / high-risk-only kept** (a Commission change, **not** the Council's). Council switches routing to the **national entry point**, adds an interim direct-notification fallback, and extends the switch-over to 30 months; the EDPB establishes the template + high-risk lists. [ST 9547/26 pt 8](../extracts/council/ST-9547-2026_gdpr-art3-amendments.md#point-8--article-33-breach-notification) |

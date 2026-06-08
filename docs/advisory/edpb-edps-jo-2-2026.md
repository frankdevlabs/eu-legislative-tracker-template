# EDPB–EDPS Joint Opinion 2/2026 (Digital Omnibus)

> **EXAMPLE advisory digest** (reference file 2025/0360) — the one worked example of the
> `docs/advisory/` layer (one digest per advisory-body opinion; `tracker.yaml` `advisory_bodies`).
> Replace with your file's opinions; delete this example. See [`SETUP.md`](../../SETUP.md).

A digest of the **joint opinion of the European Data Protection Board (EDPB) and the European Data
Protection Supervisor (EDPS)** on the *Digital Omnibus* proposal this repo tracks
(**COM(2025) 837 / 2025/0360 (COD)**). It is the regulators' formal verdict on the GDPR, EUDPR, ePrivacy
and Data-Acquis changes, delivered on the Commission's Art 42(2) EUDPR consultation.

> Source: committed opinion
> `../../sources/edpb-edps/EDPB-EDPS-JO-2-2026_opinion_2026-02-10.pdf`
> · authoritative copy on the
> [EDPB website](https://www.edpb.europa.eu/our-work-tools/our-documents/edpbedps-joint-opinion/edpb-edps-joint-opinion-22026-proposal_en).
> Working digest — verify against the authoritative text. The EDPB and the EDPS are **independent advisory
> bodies**; this opinion is **not** part of the Commission proposal and is **not** binding on the
> co-legislators. Paragraph numbers (¶) below refer to the opinion.

## Document facts

- **Reference:** EDPB–EDPS Joint Opinion **2/2026**; **adopted 10 February 2026**.
- **Legal basis:** Article 42(2) of Regulation (EU) 2018/1725 (**EUDPR**) — the Commission formally
  consulted the EDPB and the EDPS on **25 November 2025**.
- **Scope:** the data/cyber strand — **GDPR** (Reg. (EU) 2016/679), **EUDPR** (Reg. (EU) 2018/1725),
  **ePrivacy Directive** (2002/58/EC), the **Data Act** (Reg. (EU) 2023/2854) and the acquis merged into it
  (**Data Governance Act**, **Open Data Directive**, **Free Flow of Non-Personal Data Regulation**), plus
  the cyber single-entry point under **NIS2**. Unless stated otherwise, the comments on GDPR amendments
  apply equally to the corresponding **EUDPR** amendments (¶10).
- **Companion:** the AI strand (COM(2025) 836 / 2025/0359) is referenced only where the regimes interact
  (e.g. the proposed AI-Act Art 4a bias-detection rule vs GDPR Art 9(2)(k), ¶52).

## Overall stance

The EDPB and the EDPS **support** the Proposal's aims — simplifying compliance, strengthening the exercise
of individual rights, and boosting competitiveness — echoing the EDPB's **Helsinki Statement** (2 July
2025). They stress simplification must **clarify obligations and bring legal certainty while maintaining a
high level of protection** (Art 8 Charter, Art 16 TFEU). They **regret the absence of a full impact
assessment** and recommend close attention to fundamental-rights effects in future Art 97 GDPR reviews
(¶7). Recommendations fall into three buckets: **welcomed**, **strongly opposed**, and **supported in aim
but needing improvement**.

# I. GDPR and ePrivacy Directive

<a id="personal-data"></a>
## Definition of personal data — **strongly opposed** (¶11–21)

The proposed addition to Art 4(1) GDPR / Art 3(1) EUDPR (information is not personal for an entity that
cannot identify the person, and does not become personal merely because a *subsequent recipient* could)
**goes far beyond a "technical amendment" or a codification of CJEU case-law**:
- It is a **selective codification** of a single element of a single case (*EDPS v SRB*, C-413/23 P) that
  **misreads** the judgment — the CJEU held that otherwise-impersonal data become personal **both** for a
  recipient with means to identify **and, indirectly, for the entity making them available** (¶16).
- It would **narrow the concept of personal data**, invite controllers to engineer loopholes out of GDPR
  scope, and overlook "singling out" (Recital 26) — especially in online advertising (¶17).
- A **"negative" definition** ("what personal data is not") using undefined terms ("entity") **increases**
  uncertainty; risks knock-on effects on Directive (EU) 2016/680, Convention 108+ and adequacy (¶18–20).
- Open questions are **better handled by forthcoming EDPB pseudonymisation/anonymisation guidance** than by
  amending the definition (¶19).

→ **They strongly urge the co-legislators not to adopt the change** (¶21).
See Art 4 provision.

<a id="implementing-act-pseudonymisation"></a>
## Pseudonymisation by implementing act (Art 41a) — **opposed** (¶22–25)

Proposed Art 41a would let the **Commission** set, by **implementing act**, the means/criteria for when
pseudonymised data are no longer personal for certain entities. The EDPB and the EDPS object: delineating
personal data **defines the material scope of EU data-protection law**, which must rest with **independent
supervisory authorities under judicial control** (Art 8(3) Charter) and the EDPB's consistency role, not
the Commission. The "may be used as an element" wording leaves the legal effect (rebuttable presumption?
one factor?) unclear. → **Delete Art 41a** (¶25).
See pseudonymisation & data-protection-by-design provision ·
Art 4 provision.

<a id="scientific-research"></a>
## Scientific research — **welcomed, with improvements** (¶26–35)

Welcome the new **definition** and the clarification that further processing for research is compatible
**independent of Art 6(4)** (¶30). Suggestions: move the *methodological/systematic, autonomous,
verifiable, transparent* criteria **from recitals into the enacting terms**; move "innovation / commercial
interest" phrases **out of the definition** into recitals (they are context, not qualifying criteria, and
risk excluding humanities/social-science research) (¶29); extend the **duty-to-inform derogation**
(new Art 13(5)) to data originally collected from the data subject via "where and insofar" wording (¶33).
See research/secondary-use provision.

<a id="biometric"></a>
## Biometric authentication exception (Art 9(2)(l)) — **welcomed** (¶36–38)

Welcome the new derogation for **one-to-one verification** where the biometric data/means are under the
data subject's **sole control** (e.g. on-device templates). But: necessity and proportionality still apply
— use less-intrusive methods where effective; **remove** the Recital 34 line that such processing "is not
likely to create significant risks" (large-scale use can still be high-risk); add **examples of safeguards**
instead. See Art 9 provision.

<a id="ai-legitimate-interest"></a>
## AI: legitimate interest (Art 88c) — **unnecessary; improve if retained** (¶39–45)

The EDPB **already confirmed** in **Opinion 28/2024** that legitimate interest (Art 6(1)(f)) can ground AI
development/deployment on the current GDPR, so a **standalone article is not necessary** — a recital would
be more appropriate, and "may … where appropriate" adds nothing (¶39). If retained, the EDPB and the EDPS
recommend: state expressly that **all Art 6(1)(f) conditions (the three-step test) must be met** and drop
"where appropriate" (¶41); move the **right to object into Art 21 GDPR** (not a new provision), brought to
data subjects' attention in advance, and clarify the "unconditional" right goes beyond Art 21(1) (¶42);
define "**enhanced transparency**" as information *additional* to Arts 13–14 (¶43); do not conflate
mitigating measures with mandatory GDPR compliance measures (¶44); **define "operation"** of an AI system
(undefined in GDPR and the AI Act) (¶45).
See Art 88c provision.

<a id="ai-special-categories"></a>
## AI: incidental/residual special-category data (Art 9(2)(k), 9(5)) — **welcomed, improve** (¶46–52)

Acknowledge that training/testing/validating certain AI (e.g. general-purpose models) **cannot always
avoid** residual/incidental processing of special-category data. Improvements: put "**incidental and
residual**" **in the enacting terms** of Art 9(2)(k) (¶48); **bound the scope** — it should **not** cover
special-category data collected via **prompts at deployment** (¶49); make Art 9(5) require that **deletion
is impossible or disproportionate**, on a **documented, state-of-the-art** assessment (¶50); require
**lifecycle safeguards** and a bar on **re-use for other purposes** (¶51); clarify the **interplay with the
AI-Act Art 4a** bias-detection regime (¶52).
See Art 9 provision.

<a id="access-requests"></a>
## Right of access — abusive requests (Art 12(5) & 57(4)) — **improve** (¶53–59)

Welcome clarifying "abuse of rights", **but** the wording must **not** tie abuse to exercising access **for
purposes other than data protection** — the GDPR (Art 1, Art 8 Charter) protects *all* fundamental rights,
and the CJEU allows access without stating a motive (C-307/22) (¶54). Instead, link "abusive requests" to
an **abusive intention** (e.g. intent to harm the controller) (¶55). Remove "overly broad and
undifferentiated requests … excessive" from Recital 35; let data subjects **specify/clarify** before
refusal (¶56, ¶58). **Drop "reasonable grounds to believe"** and keep the current burden-of-proof threshold
(¶57). Critically, **keep Art 12(5) mirrored in Art 57(4)** so DPAs can refuse/charge on the same
conditions — and address SA **resourcing** (¶59).
See Art 12/57 provision.

<a id="transparency-derogation"></a>
## Transparency derogation (Art 13(4)) — **improve** (¶60–64)

Welcome simplifying information duties (esp. for SMEs) where the data subject already has the information,
**but** clarify "**not data-intensive activity**" and "**clear and circumscribed relationship**" (¶62);
**drop "reasonable grounds to assume"** (¶62); require that the controller **still provide full Art 13 info
on request**, and tell the data subject so (¶63); and **align EUDPR Art 15(4)** with the result (¶64).
See research/secondary-use provision ·
EUDPR mirror.

<a id="automated-decisions"></a>
## Automated decision-making (Art 22) — **retain the in-principle prohibition** (¶65–72)

The CJEU treats Art 22(1) as a **prohibition in principle** (C-634/21, *SCHUFA*), not merely a right to be
invoked — so the rewrite into an "exhaustive list of permitted cases" should keep **prohibition-with-
exceptions** wording ("a decision … shall not be based solely on automated processing … unless …") and
Recital 38 should confirm Art 22 **remains an invokable right** (¶66–67). Welcome clarifying contractual
necessity, **but** keep "regardless of whether the decision could be taken otherwise than by solely
automated means" **only in Recital 38, not the enacting terms**, and confirm ADM is "necessary" only where
**no equally effective, less-intrusive means** (automated or not) exist — consistent with Arts 5(1)(c) and
6(1)(b) (¶70–72).
See Art 22 provision.

<a id="breach-notification"></a>
## Data-breach notification (Art 33) — **welcomed** (¶73–87)

Support **raising the threshold to high-risk** (¶73) and **extending the deadline 72h → 96h** (¶77) — minor
breaches flood some SAs (thousands/year) and 72h can fall over weekends; documentation (Art 33(5)) and
Art 32 duties are unaffected. Recommend **more harmonisation** with shorter NIS2/DORA/eIDAS/CER timelines
(¶79). On the **common template + high-risk lists**: support them, **but** the Proposal lets the Commission
**unilaterally modify** the EDPB's drafts by implementing act ("after due consideration") — instead
**entrust the EDPB with both preparation *and* approval** (like the European Data Protection Seal), and the
**EDPS** for the EUDPR equivalents (the Commission must not shape its own obligations) (¶82–84). **Strongly
support the single-entry point (SEP)** under NIS2 Art 23a, with notification **security** safeguards, and
mirror the changes in EUDPR Art 34(1) (¶85–87).
See [Art 33 provision](../provisions/gdpr-art33-breach-notification.md) ·
single-entry point.

<a id="dpia"></a>
## DPIA lists, template & methodology (Art 35) — **welcomed; EDPB ownership** (¶88–95)

Support common EEA **DPIA lists** and a common **template + methodology** (¶88, ¶92). As with breach
notification, **entrust the EDPB (not the Commission) with preparing *and approving* the DPIA lists,
template and methodology** (¶90, ¶94); the methodology should be a broad, practical *guided process*, not a
checklist (¶93). The amendment to **EUDPR Art 39 is neither necessary nor appropriate** — the EDPS already
adopts EUI DPIA lists — so the co-legislators **should not adopt it**; an EUDPR methodology should be
adopted by the **EDPS** (¶91, ¶95).
See Art 35 DPIA provision · EDPB governance.

<a id="eprivacy"></a>
## ePrivacy: protection of terminal equipment (Art 88a / Art 5(3)) — **support, fragmentation concern** (¶96–107)

**Strongly support** tackling **cookie-banner / consent fatigue** and entrusting oversight to the **GDPR
supervisory authorities** (¶96). **Main concern:** splitting terminal-equipment rules across instruments
(GDPR/EUDPR for personal data, ePrivacy for non-personal) creates a **two-regime fragmentation** —
uncertainty over which rules apply and which authority supervises (¶97–98). Detailed points: regulate
**subsequent processing** consistently and clarify "purposes" (¶99–100); **delimit the new consent
exceptions** (explicitly-requested service, **audience measurement**, **security**) to what is *strictly
necessary* — audience measurement must be **aggregated/anonymous, own-use only, not shared/combined**, and
security updates must be discrete, pre-notified and switch-off-able (¶101–103); **add a contextual-
advertising exception** (more privacy-friendly than behavioural), clearly limited and safeguarded
(¶104); define a **maximum consent-validity period** and an exception to record a consent refusal without a
unique identifier (¶105–106). **Crucially, oversight needs effective corrective/fining powers** — add
references in Art 83(5) GDPR / Art 66(3) EUDPR (¶107). The **repeal of Art 4 ePrivacy Directive** (security
of processing) is welcomed to avoid overlap (¶118).
See cookies provision.

<a id="machine-readable-signals"></a>
## ePrivacy: machine-readable choices (Art 88b) — **strongly welcomed, broaden** (¶108–117)

**Strongly welcome** automated, machine-readable indications of choices to address cross-site consent
fatigue (¶108). Recommendations: cross-reference Art 88a; clarify "controllers" covers **all** (incl.
third-party cookie providers) (¶111); **no consent-by-default** — prompt on first use (¶113); set a
**timeframe** to develop/publish the standards (¶113); **do not exempt SME browser providers** (¶114);
**extend** the duty beyond browsers to **operating systems and other software** (¶115); **remove the
media-service exemption** (treat them like other providers, since it undermines the anti-fatigue aim)
(¶116); and provide **effective fining powers** for browsers/OS providers (¶117).
See cookies provision.

# II. Data Acquis (Data Act / DGA / ODD)

The EDPB and the EDPS **welcome** merging the Data Acquis into the Data Act and the streamlining of
overlapping/outdated rules (¶119–121); the opinion addresses only the most data-protection-relevant points.

<a id="data-emergency"></a>
## Public-emergency data (Data Act Art 15a) — **pseudonymise** (¶122–128)

The Proposal deletes current Art 17(2)(e), which limited public-emergency requests to **pseudonymised**
personal data and only where non-personal data are insufficient — opening the door to **non-pseudonymised**
personal data without justification (¶123). Recommend **re-inserting Art 17(2)(e)** and **deleting "where
possible"** from Art 15a(2): personal data only in **pseudonymised form**, only when non-personal data are
insufficient (¶124). Clarify "responding to" vs "mitigating/recovery"; clarify who **defines vs implements**
technical/organisational measures; and require the **EDPS** to be notified of Commission/ECB/Union-body
requests (¶125–128).

<a id="data-intermediation"></a>
## Data intermediation & altruism — **keep safeguards** (¶129–148)

While welcoming lighter regulation, recommend keeping trust/oversight safeguards: maintain a **prior
registration** requirement (at least for high-risk processing) (¶131); retain key data-intermediary
obligations (consent tools, activity logs, anti-fraud procedures, insolvency protection) (¶133–134); on the
shift to **functional (not legal) separation**, add **verifiable criteria** and apply it to *all* other
activities, with no blanket micro/small-entity exemption (¶135–138); keep **record-keeping/reporting** for
data-altruism organisations (¶139–143); **harmonise the registration application form** EU-wide via
implementing act (¶144–146); and keep competent authorities' **discretion** to prioritise enforcement
(¶147–148).

<a id="public-sector-reuse"></a>
## Re-use of public-sector data (new Chapter VIIc) — **keep DGA safeguards** (¶149–155)

Welcome consolidating the ODD and DGA into the Data Act (¶149). **Re-insert DGA Art 1(2)** ("no obligation
to allow re-use") and an **Art 1(3) equivalent** ("creates no legal basis for processing personal data; does
not affect the GDPR") (¶151–152); clarify the relationship between the access regimes (¶153); and justify /
delimit the new "**other forms of preparation of personal data**" allowing re-use **without anonymisation**
(data-minimisation concern) (¶154–155).

<a id="data-enforcement"></a>
## Enforcement & cooperation — **clarify SA role** (¶156–165)

Clarify how the new Chapters relate to the horizontal Chapter IX (designation of competent authorities,
complaints, redress) (¶157–159). **Re-insert Art 38(3)** and add an **explicit legal basis for
cross-regulatory information exchange** between Data Act competent authorities and GDPR supervisory
authorities (¶160–162). Clarify (Arts 37(3), 40(4)) that **DPAs participate on the basis of their existing
GDPR competences only**, with a **duty for Data Act competent authorities to consult the DPA** on data-
protection questions (e.g. what is personal data, whether a GDPR legal basis exists) (¶163–165).

<a id="edib"></a>
## European Data Innovation Board (EDIB) — **welcomed** (¶166–172)

Support the EDIB's increased structural flexibility and its confirmed role in consistent Data Act
application (¶167–168). Reinstate its **information-exchange / cross-border coordination** task (¶169);
clarify the EDIB **advises and assists the Commission on guidelines and standards**; and **empower the
Commission to issue guidelines on any Data Act topic**, enabling **joint EDPB–Commission guidelines** where
personal data are concerned (Art 8(3) Charter) (¶170–172).

---

## Cross-cutting recommendations

1. **Keep scope-defining rules in primary law, not implementing acts** — definition of personal data
   (Art 4), pseudonymisation criteria (Art 41a).
2. **Entrust the EDPB (and the EDPS for the EUDPR) with both preparing *and approving*** the breach
   template, breach high-risk lists, DPIA lists, DPIA template and methodology — not the Commission.
3. **Preserve CJEU-anchored protection levels** — broad concept of personal data, Art 22 prohibition-in-
   principle, access without stated motive.
4. **Effective enforcement** — fining powers for the new ePrivacy/terminal-equipment rules; adequate SA
   resourcing; cross-regulatory information exchange.
5. **Pseudonymisation as the default** for compelled data sharing (public emergencies).

---

**See also:** [Stakeholders](../stakeholders.md) · [Institutional positions](../institutional-positions.md) ·
[Fault lines](../fault-lines.md) · EESC opinion digest ·
[Commission proposal digest](../commission-proposal.md)

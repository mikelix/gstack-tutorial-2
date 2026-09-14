# Review 02 — Spec (`/spec`)

> **Status: reference example.** The decomposition below is the one that actually ran.
> Your W-numbers may differ; the property that matters is that **every item names the
> gate that judges it**. An item no gate can judge is not engineering work, it is a wish.

```
Date:            2026-08-22
Reviewer role:   PM
Command:         /spec
Scope reviewed:  CEO decisions D1-D5; work breakdown for Phases 2-5
Verdict:         PASS (with two escalations, see §Escalations)
```

---

## Fixed constraints (given, not negotiable)

- Magic **8.3.681** (`4432d7e`) · Netgen **1.5.323** (`bb8a610`) · open_pdks **1.0.572** (`54435919`) · Microlane `87079e7f6`
- Gates **5 / 6 / 7A / 7B-1R2** must pass with log artifacts
- GDS must be byte-reproducible; SHA-256 recorded every run
- Two domain agents resident: AI GDS-Architect (digital), Senior Analog IC Architect (analog)

---

## Work items

| ID | Work item | Owner | Input | Output | Judged by | Est. | Blocked by |
|---|---|---|---|---|---|---|---|
| W1 | Toolchain install + `VERSIONS.lock` | DevOps | pinned tags | `VERSIONS.lock`, resolvable binaries | Checkpoint 2 | 2–4 h | — |
| W2 | Agent install + handoff contract | DevOps | agent specs | 2 agents callable in WorkBuddy | Checkpoint 1 | 0.5 h | — |
| W3 | `config.env` + isolated launcher | Engineer | W1 paths | launcher runs under `env -i` | launcher runs | 1 h | W1 |
| W4 | P&R to GDS | **AI GDS-Architect** | Verilog, PDK, W3 | `<design>.gds` | Gates 5, 6 | 2–3 h | W1, W3 |
| W5 | Non-circular reference export | **AI GDS-Architect** | live P&R DB | `*_from_db.v` | artifact exists **and** is provably not GDS-derived | 1 h | W4 in progress |
| W6 | LVS pair (7A structural, 7B-1R2 Netgen) | **AI GDS-Architect** | GDS + W5 netlist | 2 gate logs | Gates 7A, 7B-1R2 | 1.5 h | W4, W5 |
| W7 | Determinism proof | QC | W4 twice in clean shells | identical SHA-256 | SHA match | 1 h | W4 |
| W8 | Analog sizing + sim *(optional track)* | **Senior Analog IC Architect** | spec, PDK models | sizing table + ngspice | ngspice sim | 2–4 h | W1 |
| W9 | Bilingual docs + release package | DevOps | all above | EN+ZH md/docx/pptx, zip | DoD §0.7 | 2 h | W6, W7 |

**Total: 13–18 h** including contingency. The CEO's 10–14 h budget was optimistic;
this review raised it rather than silently cutting scope.

---

## Critical path

```
W1 ─► W3 ─► W4 ─► W5 ─► W6 ─► W9
              └──► W7 ───────┘
W2 ────────────────────────────┘
W8 (parallel, off critical path)
```

W5 sits **inside** W4, not after it. The reference export must be hooked *before*
GDS stream-out; if you sequence it after, you have already built the circular
comparison you are trying to avoid.

---

## Escalations to the domain agents

Per the defer clause, the following were **not** decided by this role:

| # | Question | Referred to | Why this role cannot decide |
|---|---|---|---|
| E1 | Is Gate 7B-2 (device-level LVS) achievable with the rule decks shipped in SKY130A, or does it need new work? | **AI GDS-Architect** | Requires reading the PDK rule deck. |
| E2 | Does W5's export belong pre- or post-`gds_streamout`? | **AI GDS-Architect** | Determines whether the LVS is diagnostic or circular. |
| E3 | Should W8 be gated at all in v1.0? | **Senior Analog IC Architect** | Analog verification semantics. |

All three were answered by the domain agents and recorded in
[`03-eng-review.md`](03-eng-review.md) §Escalation responses. **This review did not
proceed until they were.**

---

## Blocking issues

None at filing time. Two noted risks escalated to the CEO in 01: install drop-out
(B3) and the un-implemented 7B-2 (B2).

---

## Non-blocking notes

- W1 should produce `VERSIONS.lock` **before** any other work starts. Recording
  versions after the fact is how "it worked yesterday" bugs are born.
- W7 is cheap and is the single most persuasive artifact in the whole project. Do it
  even if time is short.
- W8 is the only item with no gate. That is a known, stated limitation — see
  [`05-ship.md`](05-ship.md).

---

## Decisions recorded (do not relitigate in later phases)

| # | Decision |
|---|---|
| S1 | `starter/` is a **pointer, not a payload**. The tools are multi-GB; this repo does not vendor them. |
| S2 | Gates are numbered 5/6/7A/7B-1R2 to preserve compatibility with the upstream product's numbering. Gaps 1–4 are historical; do not renumber. |
| S3 | Two platforms ⇒ **two published baselines**. The VM SHA will differ. Do not force them to match. |
| S4 | `PYTHONHASHSEED=0`, seeded RNG, frozen GDS timestamp. All three, every run. |

---

## What was NOT reviewed

- The correctness of any PDK rule deck (domain-agent territory).
- Analog sizing methodology (W8, deferred to the analog agent).
- Licence text of bundled third-party components (checked at ship, review 05).

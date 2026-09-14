# gstack-tutorial-2 — Build an Open-Source End-to-End EDA System with 2 AI Agents

[![repo self-check](https://github.com/mikelix/gstack-tutorial-2/actions/workflows/selfcheck.yml/badge.svg)](https://github.com/mikelix/gstack-tutorial-2/actions/workflows/selfcheck.yml)
[![Licence: CC BY 4.0 / Apache-2.0](https://img.shields.io/badge/licence-CC%20BY%204.0%20%2F%20Apache--2.0-blue.svg)](LICENSE.md)

> **What this is.** A hands-on tutorial: use the **gstack** agent workflow plus **two
> domain AI agents** to build, run and verify a real open-source silicon flow —
> RTL → GDS on the SkyWater SKY130 open PDK — with a verification gate chain that
> locks the output down to a byte-level hash.
>
> **What this is not.** Not a Cadence-grade sign-off course. Not a toy.

Chinese version: [`README.zh.md`](README.zh.md)

---

## 0. Why a second tutorial

[gstack-tutorial-1](https://github.com/mikelix/gstack-tutorial-1) teaches the
gstack Team Mode review loop using a one-line `hello_world.py`. It is excellent at
what it does, and it deliberately carries **no real artifact**.

This tutorial keeps that skeleton and changes two things:

| | Tutorial #1 | Tutorial #2 |
|---|---|---|
| Carrier | `hello_world.py` | a real RTL→GDS EDA system |
| Team | 5 gstack **review** roles | 5 gstack roles **× 2 domain agents** |
| Proof of done | review notes merge | **gate chain PASS + GDS SHA match** |
| Environment | none | reproducible open EDA + open PDK |
| Value narrative | — | a system independently valued at ~RMB 1.25 M |

The one-line difference: **in #1 the agents review the work; in #2 the agents do
the work and are held to a verification gate.**

### The second difference — and the more important one

In #1, five gstack roles were *enough*, because the artifact was trivial. In #2
they are not, because the artifact is silicon.

> **The gstack roles are process experts and domain generalists.** They have no
> semiconductor engineering expertise and no model of a semiconductor design flow.
> They will accept `LVS passed` without knowing the check can be circular; reorder
> build steps and silently break byte-level determinism; and propose relaxing a
> tolerance to reach green.
>
> **The two domain agents own what the orchestration layer lacks** — semiconductor
> physics and flow semantics. So this is not "5 + 2". It is a **two-key system**:
> process authority sits with gstack, physics authority sits with the domain
> agents, and **on conflict, physics wins.**

Full contract: [`docs/expertise_division.md`](docs/expertise_division.md)
(中文 [`docs/expertise_division.zh.md`](docs/expertise_division.zh.md)) —
RACI table, three veto rules, escalation protocol, and a copy-paste **defer
clause** for every gstack prompt.

---

## 1. The three-layer model

```
  gstack orchestration          /plan-ceo-review → /spec → /plan-eng-review
  (review & decision audit)       → /qa-only → /ship
            │
            ├──────────────► 2 domain agents
            │                 • AI GDS-Architect          (digital: RTL→GDS, DRC/LVS)
            │                 • Senior Analog IC Architect (analog: sizing, sim, layout)
            │
            └──────────────► open EDA + open PDK + 7-gate verification chain
                              Magic · Netgen · Klayout · ngspice · Xschem
                              SKY130A · Microlane P&R
```

Nothing in the middle layer is decorative: each agent has a **handoff contract**
and every deliverable it produces is stopped by a gate.

---

## 2. Why SKY130 and not a commercial PDK

The author holds NDA-bound PDKs (TSMC, UMC, GlobalFoundries, ams 0.35 µm,
CanSemiconductor). **None of them can appear in this repository.**

1. An NDA PDK cannot be published, redistributed, or committed.
2. An "open-source tutorial" that ships a closed PDK is not open source — it is a
   leak with a README.
3. SKY130 is the first foundry-grade PDK released under an open licence, **with
   open DRC/LVS/RCX rule decks**, so every gate here can be re-run, audited and
   forked by the reader.
4. Nothing is lost: the method is process-agnostic — gate structure, determinism
   contract and agent workflow transfer to any PDK, including the closed ones.

> This section is itself the lesson. It teaches "what may be open-sourced" using a
> decision the author actually had to make.

---

## 3. Definition of Done (hard, not aspirational)

| # | Criterion | Evidence |
|---|---|---|
| 1 | Gate 5 — Magic DRC | PASS, 0 violations |
| 2 | Gate 6 — Magic extraction | PASS |
| 3 | Gate 7A — structural LVS | PASS |
| 4 | Gate 7B-1R2 — Netgen hierarchical LVS | PASS — `Circuits match uniquely.` |
| 5 | **Determinism** | GDS SHA-256 reproducible across runs |
| 6 | **Bilingual docs** | EN + 简体中文 manual shipped |

If any line fails, the tutorial is not finished. No "mostly done".

---

## 4. Two disciplines this tutorial teaches

**a) Lock the artifact.** Pinned tool versions + `PYTHONHASHSEED=0` + seeded RNG +
frozen GDS timestamp ⇒ byte-identical output. The gate chain is the referee.

**b) Check the number, not just the status.** A gate can pass and the physics still
be wrong. Two worked examples ship with this tutorial:

| Case | Predicted | Measured |
|---|---|---|
| Quadcopter hover power (GDA) | 127.8 W | 127.4 W (0.29 %) |
| CTC capture critical capillary number | Ca\* = 0.043 | 0.04 ± 0.006 |

Both survive first-principles cross-checks — and both state their falsifiable
assumption openly (e.g. the propeller figure of merit is taken independently,
**not** fitted to that flight).

---

## Pinned toolchain (do not drift)

| Tool | Version | Commit |
|---|---|---|
| Magic | **8.3.681** | `4432d7e` |
| Netgen | **1.5.323** | `bb8a610` |
| open_pdks / SKY130A | **1.0.572** | `54435919` |
| Microlane | — | `87079e7f6` |

A version change invalidates the reference SHA. Re-baseline deliberately, publish
the new baseline, and never "fix" a hash mismatch by relaxing the check.

---

## 5. Repository layout

| Path | Purpose |
|---|---|
| **[`TUTORIAL.md`](TUTORIAL.md)** | **the step-by-step course (start here)** |
| [`START_HERE.md`](START_HERE.md) | Solo and team entry points |
| [`PLAN.md`](PLAN.md) | Scope, phases, team topology, DoD |
| [`COLLABORATOR_GUIDE.md`](COLLABORATOR_GUIDE.md) | Fork model, channels, review cadence |
| [`docs/gate_chain.md`](docs/gate_chain.md) | Gate-by-gate reference |
| [`docs/expertise_division.md`](docs/expertise_division.md) | **Why gstack cannot decide domain questions** — RACI, veto rules, defer clause |
| [`docs/two-key-authority.svg`](docs/two-key-authority.svg) (+ `.png`) | The two-key authority model as one figure (embedded in the tutorial, Word and deck) |
| [`starter/`](starter/README.md) | **runnable skeleton** — gate scripts, `db_export.py`, config template |
| [`reviews/`](reviews/README.md) | **five worked gstack review records** (CEO → spec → eng → QA → ship) |
| `.github/ISSUE_TEMPLATE/weekly_progress_report.md` | Weekly report template |
| `.github/workflows/selfcheck.yml` | CI: required files, pin consistency, circularity guard |

### Deliverables (three formats)

| Format | English | 简体中文 |
|---|---|---|
| Markdown | [`TUTORIAL.md`](TUTORIAL.md) | [`TUTORIAL.zh.md`](TUTORIAL.zh.md) |
| MS Word | [`dist/gstack-tutorial-2_EN.docx`](dist/gstack-tutorial-2_EN.docx) | [`dist/gstack-tutorial-2_ZH.docx`](dist/gstack-tutorial-2_ZH.docx) |
| PowerPoint (39 slides) | [`dist/gstack-tutorial-2_EN.pptx`](dist/gstack-tutorial-2_EN.pptx) | [`dist/gstack-tutorial-2_ZH.pptx`](dist/gstack-tutorial-2_ZH.pptx) |

The markdown is the source of truth; the Word and PowerPoint files are generated
from it (see `_build/`). Change the markdown, then regenerate — do not hand-edit
the binaries.

---

## 6. Credits (stand on these shoulders)

| Project | Role |
|---|---|
| [google/skywater-pdk](https://github.com/google/skywater-pdk) | the open foundry-grade PDK |
| [RTimothyEdwards/open_pdks](https://github.com/RTimothyEdwards/open_pdks) | PDK build/install framework |
| [Magic](https://github.com/RTimothyEdwards/magic) · [Netgen](https://github.com/RTimothyEdwards/netgen) | DRC / extraction / LVS |
| [Microlane](https://github.com/htfab/microlane) | lightweight open place-and-route |
| [Tiny Tapeout](https://tinytapeout.com) (Matt Venn, Uri Shaked) | low-cost tape-out shuttle |
| [Zero to ASIC Course](https://zerotoasiccourse.com) | teaches the same tools without AI agents |
| [SiliWiz](https://app.siliwiz.com) | browser-level silicon intuition (Apache-2.0) |

**Positioning:** Zero to ASIC teaches humans to design chips with open tools.
This tutorial teaches how to run the same flow with **gstack + two domain agents**,
with the output locked by a gate chain and a hash. Adjacent layers, not competitors.

---

## 7. Licence

Prose under **CC BY 4.0**, code under **Apache-2.0** (see [`LICENSE.md`](LICENSE.md)).
The commercial `e2e-ic-system` product referenced by this tutorial is **not**
included and remains separately licensed.

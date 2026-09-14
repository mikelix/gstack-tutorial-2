# The Expertise Gap and the Authority Contract

**Why the gstack orchestration team must work with domain agents — and never
above them.**

Part of `gstack-tutorial-2`. See [`../TUTORIAL.md`](../TUTORIAL.md) §0.4 for the
short version.

---

## 1. The claim in one paragraph

The five gstack roles (AI CEO, AI PM, AI Engineer, AI QC, AI DevOps) are
**process experts and domain generalists**. They know how to decompose, sequence,
audit and release. They do not know semiconductor physics, EDA tool semantics, or
what a sign-off gate actually proves. The two domain agents (AI GDS-Architect,
Senior Analog IC Design Architect) are the inverse: they own the domain judgement
and the flow semantics, and they do not care about sprint structure or packaging.
**Correct team design is not "5 plus 2". It is a two-key system: process authority
sits with gstack, physics authority sits with the domain agents, and physics
authority wins every conflict.**

---

## 2. What each layer actually knows

### Layer 1 — gstack orchestration

| Knows well | Does NOT know |
|---|---|
| How to decompose a goal into filed, assignable work | Which PDK library is appropriate for a target node |
| How to challenge scope and positioning | Whether a DRC deck covered metal density |
| How to keep an audit trail of decisions | That LVS can be circular |
| How to produce a release artefact and a version tag | What makes a GDS byte-reproducible |
| How to refuse to fix while reporting (QA discipline) | What a "matched" netlist does *not* prove |

### Layer 2 — domain agents

| Knows well | Does NOT own |
|---|---|
| RTL→GDS flow semantics and their failure modes | Sprint structure, work breakdown |
| What each sign-off gate does and does not prove | Release mechanics, packaging |
| Non-circular verification construction | Positioning and commercial narrative (may veto, not author) |
| Determinism: hash seeds, frozen timestamps, RNG | Issue tracker hygiene |
| Analog: topology, sizing, simulation, layout intent | — |

### Layer 3 — the toolchain

Neutral referee. It does not negotiate. A gate either passes on its log or it
does not. This is why Layer 3 is the only layer allowed to settle a dispute
between Layers 1 and 2.

---

## 3. The authority contract (RACI)

R = responsible, A = accountable (single), C = consulted, I = informed,
**X = not permitted to decide**

| Decision | AI CEO | AI PM | AI Eng | AI QC | AI DevOps | GDS Agent | Analog Agent | Human |
|---|---|---|---|---|---|---|---|---|
| Scope and phasing | A | R | C | I | I | C | C | approves |
| Work breakdown (W1–W9) | C | A/R | C | I | I | C | — | I |
| PDK / stdcell library choice | X | X | X | X | X | **A** | C | approves |
| Tool version pins | X | records | X | X | records | **A** | **A** | I |
| Gate pass criteria | X | X | X | runs | X | **A** | **A** | I |
| Waiver of a DRC violation | X | X | X | X | X | **A** | C | **signs** |
| Interpretation of an LVS mismatch | X | X | reports | reports | X | **A** | C | I |
| Determinism contract | X | records | X | X | records | **A** | — | I |
| Release content and version | C | C | I | C | **A** | C | C | approves |
| Roadmap / marketing claims | drafts | drafts | X | X | drafts | **vet** | **vet** | approves |
| Any statement containing a physics number | X | X | X | X | X | **A** | **A** | I |

Read the **X** column first. It is the point of the table.

---

## 4. Three veto rules

1. **Domain veto beats process convenience.**
   If the domain agent says a step is unsafe, the step does not happen,
   irrespective of what the plan, the backlog, or the schedule says.

2. **A gate result is not a fact until the domain agent has read the log, not the
   status line.**
   `PASS`, `Circuits match uniquely.`, `DRC clean` are strings. The log is the
   evidence. AI QC is permitted to *report* a status only after the domain agent
   has *read* the log.

3. **No check is ever relaxed to make a build pass.**
   When a gate fails, either the artefact is wrong or the gate is wrong. The
   domain agent states which, in writing. Nobody silently loosens a tolerance,
   widens a window, or deletes a rule from a deck.

---

## 5. Escalation protocol (worked example)

**Symptom.** `/qa-only` reports Gate 7B-1R2 PASS with `Circuits match uniquely.`

**Naive response.** Accept. Close the item. Ship.

**Correct response.**

| Step | Actor | Action |
|---|---|---|
| 1 | AI QC | Report status **plus** confirm the reference netlist's provenance |
| 2 | AI GDS-Architect | Read the log. Establish: was the reference source emitted from the live P&R DB *before* stream-out, or extracted from the GDS itself? |
| 3 | — | If from the GDS: the check is circular. Status is **not** PASS. It is VOID. |
| 4 | Domain agent | State in writing which is wrong: the artefact or the gate |
| 5 | AI PM | File the finding as a work item; do not reword the report |
| 6 | Human | Sign |

The single sentence that makes this work:

> **"PASS" is a string. The log is the evidence.**

---

## 6. Five anti-patterns

| Anti-pattern | Why it fails | Correct form |
|---|---|---|
| Letting AI Engineer choose the PDK library | It optimises for "a library exists", not electrical fit | GDS agent decides; human approves |
| Letting AI QC certify a gate it re-ran itself | Removes the only defence against confirmation bias | Domain agent reads log, QC reports, human signs |
| Asking AI CEO to write the physics claim | Produces confident, plausible, wrong numbers | CEO drafts, domain agent vets, human approves |
| "Relax the tolerance, we're behind schedule" | Destroys the one thing the gate chain exists to provide | Never. Escalate instead |
| Treating the domain agents as reviewers | Wastes them. They are producers, not commenters | Give them a work item with an artefact and a gate |

---

## 7. The defer clause (copy-paste)

### English

```text
CONSULT REQUIRED. Before you finalise any statement about DRC, LVS, extraction,
determinism, or PDK rules, hand that specific claim to the domain agent
(AI GDS-Architect for digital, Senior Analog IC Architect for analog) and quote
its answer verbatim.

If the domain agent contradicts you, the domain agent wins. Do not resolve the
conflict yourself — escalate to the human with both statements side by side.
```

### 中文

```text
需征询领域智能体。在你敲定任何涉及 DRC、LVS、提取、确定性或 PDK 规则的表述之前，
先将该具体论断交给领域智能体（数字方向交给 AI GDS-Architect，模拟方向交给
资深模拟 IC 设计架构师），并逐字引用其答复。

若领域智能体与你的结论冲突，以领域智能体为准。不要自行裁决 ——
把两方陈述并列提交给人类裁决。
```

Attach to **every** `/plan-ceo-review`, `/spec`, `/plan-eng-review`, `/qa-only`
and `/ship` prompt in this tutorial.

---

## 8. Why the domain agents are credible

Not asserted. Evidenced.

| Evidence | Source |
|---|---|
| Gate chain with non-circular LVS (7B-1R2) | tutorial §5.3; verified run logs |
| Deterministic GDS, byte-reproducible | tutorial §6.3; `PYTHONHASHSEED=0`, frozen GDS timestamp |
| Chaotic micromixer, positive Lyapunov exponent (2002) | *Int. J. Numer. Meth. Fluids* |
| KAM torus breakdown / FTLE characterisation (2003) | *J. Micromech. Microeng.*; ASME IMECE 41389 |
| **Nonlinear dynamic analysis**, co-authored with Prof. Chih-Ming Ho (2007) | *J. Fluid Mech.* **575**, 425–448 |
| Chaotic mixer in a CTC chip — *Angewandte* cover (2011) | *Angew. Chem. Int. Ed.* **50**(13), 3084–3088 |
| Prediction vs measurement: Ca\* 0.043 vs 0.04 ± 0.006 (2019) | 2-DOF nonlinear m–c–k model |
| Prediction vs measurement: 127.8 W vs 127.4 W (0.29%) | tutorial §8.2, with FM declared independent |

The recurring pattern is **method checked against measurement, with the
falsifiable precondition stated openly**. That is the standard the orchestration
layer is being asked to respect, not to replace.

---

## 9. Generalising the pattern

This contract is not semiconductor-specific. Any domain where a wrong artefact is
expensive and a generalist cannot detect it needs the same two-key structure:

1. Identify what the orchestration layer **cannot** judge. Write it down as an
   explicit X-column.
2. Give the domain agent an **artefact and a gate**, not an advisory role.
3. Require **log reading**, not status reporting, before certification.
4. Make **relaxing a check** the one unforgivable move.
5. Put the **human signature** on waivers only.

If your domain agent produces a file no gate examines, it is doing homework, not
engineering.

---

## 10. Checklist

- [ ] Every gstack prompt in this project carries the defer clause.
- [ ] No gate status has been certified by AI QC alone.
- [ ] Every DRC/LVS waiver has a written domain-agent reason and a human signature.
- [ ] No tolerance, window or rule has been relaxed to turn a build green.
- [ ] Every public number has been vetted by a domain agent.

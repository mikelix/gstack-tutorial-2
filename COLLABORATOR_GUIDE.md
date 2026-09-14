# Collaborator Guide

How to work on this repository with other people (and with agents).

---

## 1. Repository model

| Mode | When | How |
|---|---|---|
| **Public fork** | the tutorial is released | fork → branch → PR |
| **Private fork + collaborators** | pre-release / cohort teaching | owner forks, adds collaborators, all work on the fork |

Tutorial #1 used the private-fork model successfully. Keep it if you are running
a cohort; switch to public fork on release.

---

## 2. Conductor channels

| Channel | Carries |
|---|---|
| `#ceo-review` | scope, positioning, honest-boundary decisions |
| `#qa-report` | gate results, failures, evidence |
| `#deployment` | packaging, release, docs |
| **`#gate-results`** | **new in #2** — every gate run posts its status + SHA here |

`#gate-results` is the single place to answer "is the artifact actually reproducible
right now?" without reading anyone's prose.

---

## 3. Roles and who may merge what

| Role | May merge | Must be reviewed by |
|---|---|---|
| Owner (CEO) | scope, `PLAN.md`, releases | — |
| PM | task breakdown, issues | Owner |
| Engineer | `starter/`, gate scripts | QA |
| QA | `docs/gate_chain.md`, `reviews/` | Owner |
| DevOps | packaging, docs, CI | Owner |

**No one merges their own gate results.** The person who ran the gate is not the
person who certifies it.

---

## 4. Working with the two domain agents

- **AI GDS-Architect** — digital: RTL→GDS, DRC/LVS, gate scripts.
  Its output must name the gate that will judge it.
- **Senior Analog IC Architect** — analog: sizing, simulation, layout guidance.
  Its output must state the model and its **falsifiable assumption**.

Both agents operate under a zero-hallucination rule: **every number needs a source
or a derivation; a number with neither does not enter the repo.**

---

## 5. The discipline we keep from tutorial #1

> One conceptual change = **4 files × 4 checks**.

In #2 the four files are typically: gate script · `docs/gate_chain.md` ·
EN manual · ZH manual. When you plan a change, plan all four edits.

---

## 6. Weekly report

Use the issue template at
`.github/ISSUE_TEMPLATE/weekly_progress_report.md`. Keep it to:
what shipped · gate status · SHA recorded · blockers · next week.

---

## 7. Red lines

- **No NDA material, ever.** Not a PDK file, not a screenshot, not a path.
- **No clinical/safety claims** without a citation.
- **No "mostly passing."** A gate passes or it does not.

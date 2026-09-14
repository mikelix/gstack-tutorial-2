# PLAN — gstack-tutorial-2

Scope, phases, team topology and the Definition of Done.
Read [`START_HERE.md`](START_HERE.md) for the entry points.

---

## 1. Scope

**In scope**
- Reproducible open EDA toolchain on Windows 11 (+ macOS/Linux via the VM image)
- RTL → GDS on SKY130A with a 7-gate verification chain
- Two domain agents with an explicit handoff contract, orchestrated by gstack
- Deterministic output (byte-identical GDS) and the evidence to prove it
- Bilingual (EN + 简体中文) deliverables

**Out of scope (stated, not hidden)**
- Commercial PDKs (NDA) — see README §2
- PEX/RCX, post-layout simulation, full STA, IR/EM/antenna, device-level LVS
  (Gate 7B-2) — these are **v1.1+ roadmap**, not silent gaps
- Any claim of Cadence-grade sign-off

**Positioning (honest numbers from the valuation study)**
Teaching/research objectives: ~70–85 % covered.
Commercial sign-off: ~15–25 % — budget supplementary tools, or wait for v1.1.

---

## 2. Team topology

| gstack role | Command | Duty | Domain agent invoked |
|---|---|---|---|
| CEO / owner | `/plan-ceo-review` | scope, positioning, honest boundaries | — |
| PM | `/spec` | decompose into install / agent config / gate chain / docs | — |
| Engineer | `/plan-eng-review` | run RTL→GDS, own the gate scripts | **AI GDS-Architect** |
| QA | `/qa-only` | verify Gates 5/6/7A/7B-1R2, check the GDS SHA | **AI GDS-Architect** (verification mode) |
| DevOps | `/ship` | package, bilingual docs, release | — |
| Domain experts (resident) | — | analog sizing/sim; layout/DRC/LVS automation | **Senior Analog IC Architect** + AI GDS-Architect |

### 2.1 Why this split is mandatory, not stylistic

The five gstack roles are **process experts and domain generalists**. They have no
semiconductor engineering expertise and no model of a semiconductor design flow.
They will accept `LVS passed` without knowing the check can be circular, reorder
build steps and silently destroy GDS determinism, and propose relaxing a tolerance
to reach green.

The two domain agents own exactly what the orchestration layer lacks: semiconductor
physics and flow semantics. Therefore the team is a **two-key system**:

> **Process authority sits with gstack. Physics authority sits with the domain
> agents. On conflict, physics wins.**

Full contract (RACI, veto rules, escalation, defer clause):
[`docs/expertise_division.md`](docs/expertise_division.md) ·
[中文](docs/expertise_division.zh.md) · short form: [`TUTORIAL.md`](TUTORIAL.md) §0.4.

**Three veto rules, restated:**

1. Domain veto beats process convenience.
2. A gate result is not a fact until the domain agent has read the **log**, not the status.
3. No check is ever relaxed to make a build pass.

**The defer clause** (EN/ZH in `docs/expertise_division.md` §7) must be attached to
every gstack prompt used in Phases 1–5.

The two domain agents are **not reviewers**. They produce artifacts that the gate
chain then accepts or rejects.

---

## 3. Phases

| Phase | Owner | Output | Exit criterion |
|---|---|---|---|
| **0 — Environment** | solo | toolchain installed, `config.env` written | `magic`/`netgen` both resolve; PDK `nodeinfo.json` readable |
| **1 — CEO review** | owner | scope + positioning locked | `/plan-ceo-review` signed off |
| **2 — Spec** | collaborator | task breakdown | `/spec` filed |
| **3 — Engineering** | owner + AI GDS-Architect | GDS produced | Gates 5, 6 pass |
| **4 — QA** | collaborator + gate chain | verification evidence | Gates 7A, 7B-1R2 pass + SHA matches |
| **5 — Ship** | owner | packaged release + bilingual docs | `/ship` complete |

Time budget: **10–14 h** (excluding toolchain compile time).

---

## 4. Pinned versions (do not drift)

| Component | Version | Commit |
|---|---|---|
| Magic | 8.3.681 | `4432d7e` |
| Netgen | 1.5.323 | `bb8a610` |
| open_pdks / SKY130A | 1.0.572 | `54435919` |
| Microlane | — | `87079e7f6` |

Expect a **different** PDK build (`bdc9412`) if you use the TinyTapeout VM image —
that chain gets its **own** reference SHA. Two platforms, two baselines.

---

## 5. Definition of Done

See README §3. Restated bluntly: **all four gates PASS + GDS SHA reproducible +
bilingual manual shipped.** Anything less is a draft.

---

## 6. Known risks

| Risk | Mitigation |
|---|---|
| Toolchain install is the biggest drop-out point | three install paths (see `starter/README.md`), Option C (VM) is 30 min |
| Version drift silently breaks the SHA | `VERSIONS.lock` + SHA recorded every run |
| Gate passes while physics is wrong | mandatory first-principles cross-check (README §4) |
| Agent output accepted without evidence | every artifact must name the gate that judged it |

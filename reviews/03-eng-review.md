# Review 03 — Engineering (`/plan-eng-review`)

> **Status: reference example.** This is the review where the domain agent and the
> orchestration layer disagreed, and the domain agent won. Read §The finding — it is
> the reason this tutorial exists.

```
Date:            2026-08-25
Reviewer role:   Engineer  (with AI GDS-Architect in the loop)
Command:         /plan-eng-review
Scope reviewed:  data flow W3-W6, artifact naming, gate placement, failure semantics
Verdict:         BLOCKED → PASS
```

---

## Escalation responses (from [`02-spec.md`](02-spec.md))

**E1 — Is Gate 7B-2 achievable with the shipped rule decks?**
> *AI GDS-Architect:* The device-level rules exist in SKY130A. The gap is in the
> **flow**, not the PDK: nothing in our chain invokes them, and no harness exists to
> compare device-level extraction against the PDK device models. **Answer: achievable,
> but it is new work — not a configuration change.** Keep it on the v1.1 roadmap and
> say so plainly. Do not describe 7B-2 as "not supported by the PDK"; that is false.

**E2 — Does W5's export belong pre- or post-`gds_streamout`?**
> *AI GDS-Architect:* **Strictly pre.** Exporting after stream-out means the
> reference netlist and the layout netlist share a common ancestor in the GDS, and
> the comparison degenerates. The hook must fire against the live
> `layout.instances` structure while the P&R database is still open.

**E3 — Should W8 be gated?**
> *Senior Analog IC Architect:* **Not in v1.0.** Analog verification is judged by
> simulation against corners plus human review of the sizing rationale. A gate that
> checks a netlist is meaningful for digital; for analog it would create false
> confidence. Simulation + explicit review is the honest answer.

---

## Data flow (as built)

```
   source.v
      │
      ▼
  Microlane P&R  ──────────────► live DB (layout.instances)
      │                                  │
      │                    [hook: db_export.py, PRE-streamout]
      │                                  ▼
      │                          reference_from_db.v
      │                                  │
      ▼                                  │
  <design>.gds                           │
      │                                  │
      ▼                                  │
  Magic extract ──► layout.spice         │
      │                                  │
      └──────────► Netgen LVS ◄──────────┘
                  (Gate 7B-1R2)
```

Two independent derivations from **one live database**. That is what gives the
comparison diagnostic power.

---

## The finding — why the first LVS result was VOID, not PASS

The first successful run reported:

```
Netgen 1.5.323 — Circuits match uniquely.
```

It was accepted for several hours. Then the domain agent was asked to read the log
rather than the status line, and found the reference netlist had been regenerated
from the GDS.

> *AI GDS-Architect:* A comparison whose two inputs share a common ancestor in the
> artifact under test is circular. Its outcome is determined by construction: it
> **cannot** fail on the class of error it is supposed to catch. This result is not
> PASS. It is **VOID** — it carries no information.

**Action taken.** The result was retracted, not quietly replaced. The export hook was
moved pre-streamout (E2) and the chain re-run.

**The general rule adopted here, and it is the intellectual core of this tutorial:**

> A gate status is a claim about a *log*, not about a *tool's summary line*. No status
> is reported until the domain agent has read the log. A circular result is **VOID**,
> never PASS.

---

## Artifact naming (stable, machine-greppable)

```
$RUN_DIR/
  <design>.gds                          Gate 4 output
  <design>.spice                        Gate 6 extraction
  reference_from_db.v                   Gate 7B-1R2 reference (pre-streamout)
  drc.log                               Gate 5
  extract.log                           Gate 6
  lvs_structural.log                    Gate 7A
  lvs_netgen.log                        Gate 7B-1R2
  VERSIONS.lock                         this run's pins
  sha256.txt                            GDS fingerprint
```

Logs are **append-only and never overwritten** within a run. A re-run writes a new
`RUN_DIR`, it does not edit the old one.

---

## Failure semantics (the question juniors never ask)

**What happens to `RUN_DIR` when a gate fails?**

| Decision | Adopted | Reason |
|---|---|---|
| Delete the run dir on failure | **No** | Destroys the evidence you need to debug. |
| Overwrite in place | **No** | Two runs sharing a path makes the SHA meaningless. |
| **Freeze the dir, write `FAILED` marker, exit non-zero** | **Yes** | Post-mortem possible; CI can assert on the marker. |
| Continue to the next gate after a failure | **No** | A downstream pass on a broken input is noise. |

Exit code contract: `0` = all gates PASS, `1` = a gate FAILED, `2` = a gate returned
VOID (circularity or unverifiable input). **VOID is its own exit code** so it cannot
be mistaken for success by a script or by a reviewer skimming.

---

## Blocking issues (at first filing)

**B4 — Circular reference source.** Gate 7B-1R2 was VOID. *Fixed by:* moving
`db_export.py` pre-streamout; re-run; result PASS with log evidence.
**B5 — Path mangling under Cygwin/MSYS.** Windows-style paths were being rewritten,
producing silently empty PDK paths. *Fixed by:* isolated launcher
(`env -i`, `MSYS2_ARG_CONV_EXCL='*'`), never a bare shell.
**B6 — Netgen argument form.** The 2-argument `lvs` form was used; Netgen requires the
4-argument Tcl form `lvs [list $f $cell] [list $f $cell] $SETUP $log`.
*Fixed by:* `run_lvs.tcl` rewritten.

---

## Non-blocking notes

- Magic emits warnings on standard-cell abutment that are expected with this library.
  They are enumerated, not suppressed. A suppressed warning is a future bug.
- Gate 7A (structural) and 7B-1R2 (hierarchical) are complementary, not redundant:
  7A catches structural divergence fast, 7B-1R2 catches connectivity and device
  mismatch. Keep both.
- `sha256sum` of the GDS is taken **after** the timestamp freeze. Freezing is part of
  the recipe, not an optimisation.

---

## Decisions recorded

| # | Decision |
|---|---|
| G1 | Reference source is exported from the live P&R DB, pre-streamout. Never from the GDS. |
| G2 | Decap/filler power-ground connectivity is taken from the authoritative PDK CDL/SPICE, not inferred from layout. |
| G3 | VOID is a first-class gate outcome with its own exit code (2). |
| G4 | Every run gets its own `RUN_DIR`. Never overwrite. |
| G5 | All tool invocations go through the isolated launcher. No bare shells. |

---

## What was NOT reviewed

- Physical correctness of the placed design (no post-layout simulation in v1.0).
- Timing, IR drop, electromigration, antenna effects — **all roadmap**.
- Gate 7B-2 (device-level LVS) — confirmed out of scope for v1.0 by E1.

---

## Addendum

**2026-08-26 — after re-run.** B4, B5, B6 closed. Gates 5, 6, 7A, 7B-1R2 PASS with
logs. GDS SHA-256 stable across two independent clean-shell runs. Verdict **PASS**.

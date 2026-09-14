# Review 04 — QA (`/qa-only`)

> **Status: reference example.** `/qa-only` **reports, it does not fix.** The value of
> this review is almost entirely in §What was NOT checked — read that section first.
>
> This report was produced by the QC role **after** the AI GDS-Architect had read the
> gate logs. Per the fourth rule (Part 6.1), QC alone is not permitted to certify a
> gate in this project.

```
Date:            2026-08-28
Reviewer role:   QA
Command:         /qa-only
Scope reviewed:  Gates 5 / 6 / 7A / 7B-1R2, determinism, packaging inputs
Verdict:         PASS
```

---

## Gate status table

| Gate | Tool | Version | Status | Artifact | Notes |
|---|---|---|---|---|---|
| 5 — DRC | Magic | 8.3.681 | **PASS** | `$RUN_DIR/drc.log` | 0 violations. No waivers. |
| 6 — Extraction | Magic | 8.3.681 | **PASS** | `$RUN_DIR/<design>.spice` | 3 abutment warnings, enumerated, expected with `sky130_fd_sc_hd`. |
| 7A — Structural LVS | Microlane comparator | `87079e7f6` | **PASS** | `$RUN_DIR/lvs_structural.log` | Structural match. |
| 7B-1R2 — Hierarchical LVS | Netgen | 1.5.323 | **PASS** | `$RUN_DIR/lvs_netgen.log` | `Circuits match uniquely.` Reference from live P&R DB (G1). |
| — Determinism | `sha256sum` | — | **PASS** | `$RUN_DIR/sha256.txt` | Two independent clean-shell runs, identical. |

### Domain-agent pre-read (mandatory before this table was written)

> *AI GDS-Architect, on `lvs_netgen.log`:* The reference netlist is
> `reference_from_db.v`, produced pre-streamout from `layout.instances`. The layout
> netlist comes from Magic extraction of the GDS. The two derivations are independent
> above the P&R database. **This comparison is diagnostic. I certify the PASS.**

Without that sentence, this table would be a restatement of tool summary lines.

---

## Determinism

```markdown
# VERSIONS.lock
magic        8.3.681   (4432d7e)
netgen       1.5.323   (bb8a610)
open_pdks    1.0.572   (54435919)
microlane    —         (87079e7f6)
platform     Windows 11 + Cygwin64
run 1 sha256 6ef1c9c9…322bf750
run 2 sha256 6ef1c9c9…322bf750   ← identical
```

**Two platforms, two baselines.** The TinyTapeout VM pins Magic `8.3.576` and a
different PDK build (`bdc9412`). Its SHA will not equal the value above. That is
**expected**, not a failure: publish both, label both, and never "fix" a mismatch by
relaxing the check.

---

## Cross-checks — the number, not just the status

A gate can pass and the physics still be wrong. Two independent first-principles
checks were run on claims adjacent to this project:

| Claim | Predicted | Measured | Error |
|---|---|---|---|
| Quadcopter hover power (momentum theory, m = 1.04 kg, 9.4 in prop) | 127.8 W | 127.4 W | 0.29 % |
| CTC capture critical capillary number Ca\* | 0.043 | 0.04 ± 0.006 | within 1σ |

Both hold. Both state their falsifiable assumption openly — the propeller figure of
merit is taken from independent measurement, **not fitted** to the flight in question.
Fitting it would have made the agreement meaningless.

---

## What was NOT checked

**This is the most important section of this report.**

| Not checked | Why it matters | Status |
|---|---|---|
| **Gate 7B-2 — device-level LVS** | Devices are compared at cell level, not at individual transistor level. A device-level error can survive this chain. | Roadmap v1.1 |
| **PEX / RCX** | No parasitic extraction ⇒ no post-layout delay. The design is connectivity-correct and DRC-clean, not timing-correct. | Roadmap v1.1 |
| **Post-layout simulation** | Nothing has been simulated against the extracted netlist. | Roadmap v1.1 |
| **STA, IR drop, EM, antenna** | Not run. Do not describe this output as taped-out-ready. | Roadmap |
| **Analog track (W8)** | Judged by ngspice + human review only. **No gate exists.** | Known gap, stated |
| **Timing across corners** | No corners were run. | Roadmap |
| **GDS semantic content** | The SHA proves reproducibility, not correctness. A reproducible wrong GDS is still wrong. | By design |
| **The PDK itself** | SKY130A is taken as ground truth. If the PDK is wrong, every gate inherits it. | Out of scope |

**Blunt summary:** this release proves *the flow is reproducible and the layout is
consistent with its own source*. It does not prove *the chip works*. Anyone who
tells you otherwise has not read this section.

---

## Blocking issues

None at this review.

## Non-blocking notes

- The three Magic abutment warnings should be written into the release notes, not
  dropped. A user who sees them and panics costs you a support email; a user who was
  told in advance costs nothing.
- `sha256.txt` should be committed alongside the release, not generated on demand.
- The exit-code contract (0/1/2) is implemented. Recommend CI assert on it so VOID
  cannot be silently swallowed.

---

## Decisions recorded

| # | Decision |
|---|---|
| Q1 | No gate result is published without a domain-agent pre-read of the log. |
| Q2 | The "what was NOT checked" table is part of every QA report. A QA report without it is rejected. |
| Q3 | Two published baselines (Windows/Cygwin, VM). Neither is "correct". |
| Q4 | CI must fail on exit code 2 (VOID), not just on 1. |

---

## What was NOT reviewed

- Documentation wording (DevOps, review 05).
- Licence compliance of third-party components (review 05).
- Any analog claim (no gate; explicitly out of scope).

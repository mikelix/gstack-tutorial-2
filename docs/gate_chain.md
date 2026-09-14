# Gate chain reference

Every gate has: **a tool, a command, a pass criterion, and an artifact.**
A gate with no artifact did not run.

---

## Gates implemented in this tutorial

| Gate | What it checks | Tool | Pass criterion |
|---|---|---|---|
| **5 — DRC** | geometry vs foundry rules | Magic 8.3.681 | 0 violations (waived rules listed explicitly) |
| **6 — Extraction** | layout → netlist | Magic 8.3.681 | extraction completes; warnings enumerated |
| **7A — Structural LVS** | P&R netlist vs gate-level netlist | Microlane comparator | structural match |
| **7B-1R2 — Hierarchical LVS** | extracted vs P&R-DB-derived source | Netgen 1.5.323 | `Circuits match uniquely.` |

### Why 7B-1R2 has a "1R2"

The naive comparison is **circular**: comparing a GDS-derived netlist against a
netlist derived from the same GDS proves nothing.

The fix: emit the reference source from the **live place-and-route database**
(`db_source_export.py`, hooked in before GDS stream-out), not from the GDS. The
comparison then has real diagnostic power.

---

## Determinism contract

| Ingredient | Value |
|---|---|
| `PYTHONHASHSEED` | `0` |
| RNG | seeded, explicit |
| GDS timestamp | frozen (1970) |
| Tool versions | pinned (see `PLAN.md` §4) |
| **Result** | byte-identical GDS ⇒ reproducible SHA-256 |

Record the SHA **every run**. Two platforms, two baselines:

- Windows/Cygwin chain → reference SHA A
- TinyTapeout VM chain → reference SHA B

Do not "fix" a mismatch by relaxing the check. Investigate it.

---

## Gates on the roadmap (v1.1+)

| Gate | What it needs | Status |
|---|---|---|
| **7B-2 — Device-level LVS** | KLayout + `libs.tech/klayout/lvs` | tool **and rules already ship with the PDK**; not yet wired into the chain |
| **8 — PEX / RCX** | `rules.openrcx.sky130A.{min,nom,max}.{magic,calibre,spef_extractor}` | rules ship with the PDK; pipeline stage missing |
| **9 — Post-layout simulation** | ngspice + extracted netlist | ngspice available; not wired |
| **10 — Full STA** | OpenLane / OpenSTA | available, **requires Docker** — keep as an optional track |

> Important correction carried into this tutorial: the open SKY130 PDK **ships DRC,
> LVS and RCX rule decks**. The PEX and device-level-LVS gaps are in **our pipeline**,
> not in the PDK. They are fixable, not closed doors.

---

## Reporting a gate result

Post to `#gate-results`:

```
gate: 7B-1R2
tool: netgen 1.5.323
status: PASS | FAIL
sha256: <gds sha>
artifact: <path>
notes: <waivers, warnings, anything a reviewer must know>
```

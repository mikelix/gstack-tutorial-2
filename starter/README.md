# starter/ — the skeleton you run

Two things live here: **install instructions** (below) and a **runnable skeleton**
(`scripts/`, `designs/`, `config.env.example`) that implements the gate chain, the
non-circular export and the exit-code contract.

The EDA tools themselves are **not** vendored — they are multi-gigabyte and upstream
licensed. This repo points at them; it does not carry them.

```
starter/
  config.env.example        → copy to config.env, edit, never commit
  versions.lock.template    → fill in BEFORE your first run, not after
  scripts/
    run_all.sh              the whole chain, one command (exit 0/1/2/3)
    run_drc.tcl             Gate 5
    run_extract.tcl         Gate 6
    run_lvs.tcl             Gate 7B-1R2
    db_export.py            the pre-streamout reference export — read this one
  designs/
    my_first_gds.v          trivial RTL (source, NOT the LVS reference)
    layout.db.json          example P&R database dump for db_export.py
```

**Try the export before you install anything:**

```bash
cd starter
python3 scripts/db_export.py \
    --db-in  designs/layout.db.json \
    --out    /tmp/reference_from_db.v \
    --marker /tmp/.db_export_marker
python3 scripts/db_export.py --db-in designs/layout.db.json --out /tmp/ref2.v --marker /tmp/.m2
diff /tmp/reference_from_db.v /tmp/ref2.v     # must be empty
```

If the two files differ, the exporter is non-deterministic and nothing downstream
can be trusted. This is the cheapest determinism test in the whole project.

---

## Three install paths

| Path | Platform | Time | Status |
|---|---|---|---|
| **A — one-click installer** (`install_eda.bat`) | Windows 11 | 1–3 h (compiles) | beta; pinned versions vendor-validated |
| **B — manual step-by-step** | any | 2–4 h | fully documented, every link listed |
| **C — TinyTapeout VM image (recommended)** | Windows / macOS / Linux | **~30 min** | upstream-maintained |

> **If you have never installed an open EDA toolchain before, use Option C.**
> Do not spend your first day compiling.

**No local disk for the VM?** (~20 GB needed.) Build a derived image in CI instead —
Packer + GitHub Actions, zero local disk. See `vm/` in the commercial package, or
roll your own from the upstream Packer template.

---

## Option C — the VM image (recommended)

Upstream: <https://github.com/TinyTapeout/analog-virtualbox-vm-sky130a> (Apache-2.0)

Contents: Ubuntu 22.04 + Magic + KLayout + Xschem + netgen + ngspice + gaw +
OpenLane + Verilator + SkyWater 130 nm PDK.

- Download `tinytapeout_analog_vm.ova` (~5 GB), verify with the published SHA-256
- Import: `VBoxManage import tinytapeout_analog_vm.ova --vsys 0 --basefolder <your path>`
  (change the default machine folder **before** importing — it defaults to your
  system drive)
- Login `ttuser` / `magic`
- **Disk warning:** the image needs ~20 GB free to import; the virtual disk is
  provisioned at 32 GB.

**Version note:** the VM pins Magic `8.3.576`, this tutorial pins `8.3.681`.
Expect a **different** GDS SHA on the VM — that is expected, not a failure.
Re-baseline and move on.

---

## Option A / B — native install

Pin exactly these (do not drift):

| Component | Version | Source |
|---|---|---|
| Magic | **8.3.681** | <https://github.com/RTimothyEdwards/magic> (tag `8.3.681`, commit `4432d7e`) |
| Netgen | **1.5.323** | <https://github.com/RTimothyEdwards/netgen> (tag `1.5.323`, commit `bb8a610`) |
| open_pdks / SKY130A | **1.0.572** | <https://github.com/RTimothyEdwards/open_pdks> (commit `54435919`) |
| Microlane | commit `87079e7f6` | <https://github.com/htfab/microlane> |

On Windows these build inside **Cygwin64**. Two gotchas that cost hours:

1. Use an isolated launcher (`env -i`, `MSYS2_ARG_CONV_EXCL='*'`) — MSYS path
   mangling otherwise corrupts Windows-style paths. `run_all.sh` does this for you.
2. Netgen's LVS takes the **4-argument Tcl form**:
   `lvs [list $f $cell] [list $f $cell] $SETUP $log`

---

## Verify before you go further

```bash
magic   -dnull -noconsole --version
netgen  -batch -nogui
cat $PDK_ROOT/sky130A/.config/nodeinfo.json     # node, feature-size, open_pdks, magic
ls $PDK_ROOT/sky130A/libs.tech                  # magic netgen klayout ngspice xschem ...
```

If all four respond, you are ready for Phase 1.

---

## The exit-code contract

`run_all.sh` returns:

| Code | Meaning |
|---|---|
| `0` | all gates PASS |
| `1` | a gate FAILED |
| `2` | a gate returned **VOID** (circular input — the reference came from the GDS) |
| `3` | environment error (bad config, missing tool, reused `RUN_DIR`) |

VOID has its own code so a script, or a reviewer skimming, cannot mistake it for
success. Make your CI fail on `!= 0`, and alert separately on `== 2`.

---

## What the commercial product adds (optional)

The `e2e-ic-system` seed package (separately licensed, **not included here**)
provides the parameterized gate scripts, the two agent specs, the bilingual
manual and the QC report — i.e. it removes the plumbing, not the learning.
This tutorial is fully completable without it.

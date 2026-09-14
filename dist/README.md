# gstack Tutorial No. 2 — deliverables

Three formats, two languages. The **Markdown is the source of truth**; Word and
PowerPoint are generated from it.

| Format | English | 简体中文 |
|---|---|---|
| Markdown (source) | [`../TUTORIAL.md`](../TUTORIAL.md) | [`../TUTORIAL.zh.md`](../TUTORIAL.zh.md) |
| MS Word | `gstack-tutorial-2_EN.docx` | `gstack-tutorial-2_ZH.docx` |
| PowerPoint (35 slides) | `gstack-tutorial-2_EN.pptx` | `gstack-tutorial-2_ZH.pptx` |
| Authority contract | [`../docs/expertise_division.md`](../docs/expertise_division.md) | [`../docs/expertise_division.zh.md`](../docs/expertise_division.zh.md) |

## The second, more important idea

The gstack orchestration roles are **process experts and domain generalists**. They
have no semiconductor engineering expertise. The two domain agents own the physics
and the flow semantics. The team is therefore a **two-key system**:

> Process authority sits with gstack. Physics authority sits with the domain
> agents. On conflict, physics wins.

This is §0.4 of the tutorial, plus five slides in each deck, plus the standalone
RACI reference in `docs/`.

## What the tutorial covers

| Part | Content |
|---|---|
| 0 | Mental model: three layers, five gstack roles, two domain agents |
| 0.4 | **The expertise gap — RACI, three veto rules, the defer clause** |
| 1 | Install WorkBuddy, gstack and the two domain agents |
| 2 | Install the open EDA toolchain (three paths, pinned versions) |
| 3 | Phase 1 — `/plan-ceo-review` sets scope |
| 4 | Phase 2 — `/spec` decomposes into W1–W9 |
| 5 | Phase 3 — `/plan-eng-review` + AI GDS-Architect runs RTL → GDS |
| 6 | Phase 4 — `/qa-only` verifies and proves determinism (SHA) |
| 7 | Phase 5 — `/ship` packages and releases |
| 8 | The two disciplines: lock the artifact · check the number |
| 9 | Bringing in the Senior Analog IC Architect |
| 10 | Troubleshooting |
| 11 | Assessment: labs, written questions, grading rubric |
| 12 | Where to go next + credits |
| A–D | Prompt library · review template · version lock card · glossary |

## Also in the repository

| Path | What it is |
|---|---|
| [`../starter/`](../starter/README.md) | **runnable skeleton** — `run_all.sh` (exit 0 PASS / 1 FAIL / **2 VOID** / 3 env), `run_drc.tcl`, `run_extract.tcl`, `run_lvs.tcl`, `db_export.py` (the pre-streamout reference export), `config.env.example`, `versions.lock.template`, `designs/` |
| [`../reviews/`](../reviews/README.md) | **five worked gstack review records** — CEO → spec → engineering → QA → ship. 03 is the one where a passing LVS was retracted as **VOID** because it was circular |
| [`../.github/workflows/selfcheck.yml`](../.github/workflows/selfcheck.yml) | CI: required files, cross-document version-pin consistency, presence of the circularity guard, exporter determinism |

The five reviews are the audit trail; read them **after** writing your own.

## Regenerating

```bash
python _build/md2docx.py TUTORIAL.md    dist/gstack-tutorial-2_EN.docx
python _build/md2docx.py TUTORIAL.zh.md dist/gstack-tutorial-2_ZH.docx
python _build/build_en.py
python _build/build_zh.py
```

Requires `python-docx` and `python-pptx`.

## Design notes

- Decks are 16:9 (13.333 × 7.5 in), navy `#061F32` / accent `#00A6C9`.
- Latin font Arial, East Asian font 微软雅黑 — set explicitly so Chinese renders
  correctly on machines without the deck author's font defaults.
- Every content slide carries a footer, a page number and a takeaway note band.

## Honest boundaries

- The digital gate chain (5 / 6 / 7A / 7B-1R2) is implemented and validated on
  Windows 11 + Cygwin. PEX/RCX, post-layout simulation, full STA and Gate 7B-2 are
  **roadmap**, and the rule decks for most of them already ship with the PDK.
- The analog agent has **no gate chain yet** — judged by simulation and human review.
- macOS/Linux execution is via the TinyTapeout VM image and produces a **different**
  GDS SHA. Publish two baselines; do not force them to match.

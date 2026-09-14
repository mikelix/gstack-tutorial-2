# START HERE

Two entry points. Pick one and do not mix them on day one.

---

## A. Solo path (recommended for the first run)

**Prerequisites**
- Windows 11 (macOS/Linux: use the VM image — see starter/README.md, Option C)
- ~20–30 GB free disk for the toolchain
- Tencent WorkBuddy installed (or Claude Code / OpenAI Codex — the agent specs
  are host-agnostic)
- 10–14 h

**Steps**

1. Read [`README.md`](README.md) §0–§3. Know what "done" means before starting.
2. `cd starter/` and follow [`starter/README.md`](starter/README.md).
   **Stop when `magic -dnull --version` and `netgen -batch` both respond.**
3. Run `/plan-ceo-review` on your scope. Do not skip this — it is where the
   honest boundaries get written down.
4. Run `/spec` to decompose. Four work items: install, agent config, gate chain,
   docs.
5. Run `/plan-eng-review` with the **AI GDS-Architect** agent active. Produce GDS.
6. Run `/qa-only`. Verify Gates 5 / 6 / 7A / 7B-1R2 and the GDS SHA.
7. Run `/ship`.

**You are done when** all four gates pass, the SHA reproduces, and the bilingual
docs exist. Not before.

---

## B. Team path

1. Fork this repo; add collaborators (see [`COLLABORATOR_GUIDE.md`](COLLABORATOR_GUIDE.md)).
2. Owner runs Phase 1 (`/plan-ceo-review`), collaborator runs Phase 2 (`/spec`).
3. Work is handed off through Conductor channels:
   `#ceo-review`, `#qa-report`, `#deployment`, **`#gate-results`**.
4. Weekly report via the issue template in
   `.github/ISSUE_TEMPLATE/weekly_progress_report.md`.

---

## The one habit that matters most

From tutorial #1, carried over verbatim:

> **One conceptual change = 4 files × 4 checks.**

A change to a gate definition touches the gate script, the docs (EN), the docs
(ZH) and the review record — and each must be re-checked. Budget for it; do not
discover it at the end.

---

## If the install fails

Do not debug alone for hours. Fall back in this order:

1. **Option C** (TinyTapeout VM) — 30 min, cross-platform
2. **Option B** (manual step-by-step) — slow, but every command is listed
3. Open an issue with the failing command and the output of
   `magic --version; netgen --version; cat $PDK_ROOT/sky130A/.config/nodeinfo.json`

# PLAYBOOK — how this tutorial was actually built

> **Audience:** whoever authors gstack Tutorial No. 3.
> **What this is:** the worked process behind `gstack-tutorial-2`, written down while
> it is still fresh, in the order the work was actually done.
> **What it is not:** a template to fill in. The content changes; the *sequence* and
> the *invariants* do not.

| | |
|---|---|
| Repo | <https://github.com/mikelix/gstack-tutorial-2> |
| Commits | 3 (`db12056` scaffold → `5aa3de8` publish → `61f5230` figure + analog sections) |
| Tracked files | 45 |
| Tutorial | EN 1195 lines / ZH 1135 lines · 61 `##` sections each · bilingual parity enforced |
| Deliverables | `TUTORIAL.md`+`.zh.md` (source of truth) → `.docx` ×2 → `.pptx` ×2 (39 slides each) |
| Releases | `v1.0`, `v1.0.1` |
| CI | `repo self-check` — 29 required files, 3 version pins, circularity guard, exporter determinism |

---

## 0. The one invariant

```
                ┌─────────────────────────────┐
   you edit ──► │  TUTORIAL.md / .zh.md       │  ◄── the ONLY source of truth
                └──────────┬──────────────────┘
                           │  _build/
          ┌────────────────┼──────────────────┐
          ▼                ▼                  ▼
   md2docx.py        build_en.py         GitHub renders
   (.docx)           build_zh.py          markdown
                     (.pptx)
```

**Never hand-edit anything in `dist/`.** Every binary there is regenerated:

```bash
PY=<python-with-docx-and-pptx>
$PY _build/md2docx.py TUTORIAL.md    dist/gstack-tutorial-2_EN.docx
$PY _build/md2docx.py TUTORIAL.zh.md dist/gstack-tutorial-2_ZH.docx
$PY _build/build_en.py      # -> dist/gstack-tutorial-2_EN.pptx
$PY _build/build_zh.py      # -> dist/gstack-tutorial-2_ZH.pptx
```

The moment someone "just fixes a typo in the .docx", the next rebuild silently
reverts it and nobody notices for a week. If a fix is needed, fix the Markdown.

---

## 1. The ten steps, in order

### S0 — Frame it with the AI CEO (`/plan-ceo-review`) *before writing anything*

The first artifact is not a chapter. It is `reviews/01-ceo-review.md`, and it must
answer three questions with numbers, not adjectives:

1. **What is in scope, and what is deliberately out** — written as a *stated* gap,
   never a silent one ("PEX/RCX is v1.1+ roadmap, not implemented" beats silence).
2. **What honest fraction of the goal does this reach** — e.g. teaching/research
   ~70–85 %, commercial sign-off ~15–25 %.
3. **What would make us kill it** — the drop-out analysis.

Run this first because it is the only step that can save you the other nine.

### S1 — Decompose with the AI PM (`/spec`)

Weeks W1–W9 with a stated critical path. Two properties that mattered:

- A task that can only be validated by running the whole chain **must be nested
  inside** the task that builds it (W5 inside W4), not sequenced after it.
- Every item whose *verdict* requires domain physics is escalated (E1/E2/E3) to a
  domain agent by name — never resolved by the PM.

### S2 — Lock the toolchain pins before writing prose

Three pins, cross-checked by CI across six documents:

| Tool | Version | Commit |
|---|---|---|
| Magic | 8.3.681 | `4432d7e` |
| Netgen | 1.5.323 | `bb8a610` |
| open_pdks | 1.0.572 | `54435919` |

Do this in S2, not later: the first time the self-check ran it caught that **both
READMEs had no version pins at all**. The check paid for itself in one run.

### S3 — Design the gate chain and its exit-code contract

```
Gate 5   Magic DRC
Gate 6   Magic extraction
Gate 7A  Microlane structural LVS
Gate 7B-1R2  Netgen hierarchical LVS
```

`starter/scripts/run_all.sh` exit codes:

| Code | Meaning |
|---|---|
| `0` | PASS |
| `1` | FAIL |
| `2` | **VOID** — the run did not prove what it claims |
| `3` | environment broken |

`VOID` having its own code is the single most important design decision in the
repo. Without it, "the gate passed" and "the gate was meaningless" both print
success, and the tutorial teaches nothing.

### S4 — Build the runnable skeleton, and make it fail loudly

`starter/` is not appendix material; it is the evidence. It contains a
**mechanised circularity guard**: if the LVS reference netlist was derived from
the GDS it is being compared against, `run_all.sh` exits `2` and never invokes
Netgen. `db_export.py` exports the reference from the live layout database
instead, and writes a marker file the guard checks.

Prove determinism mechanically (this is literally the CI job):

```bash
python3 scripts/db_export.py --db-in designs/layout.db.json --out /tmp/ref1.v --marker /tmp/m1
python3 scripts/db_export.py --db-in designs/layout.db.json --out /tmp/ref2.v --marker /tmp/m2
diff /tmp/ref1.v /tmp/ref2.v     # must be empty
```

### S5 — Write the tutorial body

Structure that worked: **Part 0 mental model → Parts 1–2 install → Parts 3–7 the
five gstack phases → Parts 8–12 disciplines, troubleshooting, assessment, next**.
Every part ends in a **Checkpoint** with checkboxes. Appendices A–D hold the
prompt library, review template, printable version-lock card, and glossary.

Two rules:
- Each gstack phase maps to exactly one review command, and the tutorial shows
  the real review file (not a toy example).
- Every claim carries a source, a derivation, or an explicit "assumption, and
  here is how you would falsify it".

### S6 — Give the domain agents their own section

Part 9 exists because the orchestration layer cannot invent physics. It carries
the ~20-phase analog workflow (`Specs → Physics → Architecture → Optimization →
Statistics → Layout → Silicon`), the explicit contrast with
`draw schematic → SPICE → layout`, and the four levels of AI use
(assistant → optimizer → layout assistant → autonomous agents).

**Rule for No. 3:** if the tutorial's subject has a domain of expertise, there is
a Part N for it, and it is written *with* the domain agent, quoted, not paraphrased.

### S7 — Write the five reviews as you go

`reviews/01-ceo-review` → `02-spec` → `03-eng-review` → `04-qa-report` → `05-ship`.
Written **at the time**, append-only, verdict one word (`PASS` / `REVISE` /
`BLOCKED`). The audit trail is the product; reconstructing it later is forgery.

The review that carried the most weight: `03-eng-review`, where the first LVS run
printed `Circuits match uniquely.` and was judged **VOID, not PASS** — because the
reference netlist had been derived from the GDS under test. That page is the
intellectual core of the whole tutorial.

### S8 — Build, then validate mechanically

```bash
python .github/scripts/selfcheck.py     # required files, pins, guards, bilingual parity
```

Then check the binaries for overflow (see §4). A slide that renders off-canvas or
a table cell that overflows its column is a defect, and it is machine-detectable.

### S9 — Ship

```
selfcheck → repackage zip → git add/commit → push → watch CI → draft release
```

Release assets: both `.docx`, both `.pptx`, plus the deliverables zip. Release
notes must restate **known gaps** — the VM-side baseline SHA and Gate 7B-2 are
absent from v1.0.1 and that is printed in the notes, not hidden.

---

## 2. The two-key authority contract (non-negotiable)

```
   gstack orchestration              two domain agents
   CEO · PM · Eng · QC · DevOps      GDS-Architect · Analog IC Architect
   ── process authority ──           ── physics authority ──
                    └──────────► gate chain ◄──────────┘
                        (neutral referee: Magic / Netgen / PDK)
                     on conflict, physics wins
```

- Process decisions (schedule, decomposition, packaging) → gstack.
- Physics decisions (DRC/LVS/extraction, PDK rules, determinism) → domain agents.
- On conflict: **physics wins**; the two statements are placed side by side and a
  human signs.
- The defer clause goes into every gstack prompt verbatim:

  > CONSULT REQUIRED. Before asserting anything about DRC, LVS, extraction,
  > determinism or PDK rules, hand the claim to the domain agent and quote the
  > reply verbatim. If it conflicts with your conclusion, the domain agent wins —
  > do not adjudicate; put both statements in front of the human.

Full text: [`docs/expertise_division.md`](docs/expertise_division.md) /
[`.zh.md`](docs/expertise_division.zh.md). Figure:
[`docs/two-key-authority.svg`](docs/two-key-authority.svg).

---

## 3. Reusable machinery

### 3.1 `deck.py` — slide primitives

| Function | Use |
|---|---|
| `slide_title` | opening / section divider with kicker + meta |
| `slide_section` | numbered part divider |
| `slide_bullets` · `slide_checklist` | lists, checkpoints |
| `slide_steps` | ordered workflow |
| `slide_table` | headers + rows (keep cells short — see §4 P9) |
| `slide_code` | code / command blocks |
| `slide_two_col` · `slide_layers` · `slide_flow` | comparisons, stacks, pipelines |
| `slide_quote` | pull-quote with attribution |
| `slide_image` | embed a raster figure |

Canvas is 13.333 × 7.5 in. Colours: `NAVY NAVY2 ACCENT ACCENT2 WHITE LIGHT GREY DARK`.
Slides are declared as a list in `build_en.py` / `build_zh.py`; the two must stay
slide-for-slide identical.

### 3.2 `md2docx.py` — supported Markdown subset

H1–H6 headings, `-`/`*` bullets, ordered lists, `- [ ]` checkboxes, fenced code,
GFM tables, `---` rules, `> ` blockquotes, `![alt](path)` images, and
`Figure N — …` captions. Anything fancier will render literally. **Write to the
subset.**

### 3.3 `svg2png.py` — the figure pipeline, and its sharp edge

`docs/two-key-authority.svg` is the source of truth; GitHub and browsers render it,
so the Markdown deliverable just links it. `python-docx` and `python-pptx`
**cannot embed SVG**, so a raster twin is needed. `svglib` + `reportlab` is the
obvious route and it does not work here (`renderPM` has no raster backend), so the
figure is re-drawn in matplotlib using the *same* coordinates, colours and text.

> **Consequence:** if you edit the SVG you must edit `LAYOUT` in `svg2png.py` by
> hand. They are not linked. This is the weakest joint in the build; do not
> "improve" the figure without re-running the render and eyeballing the PNG.

### 3.4 `.github/scripts/selfcheck.py`

Required files (29), version-pin consistency across documents, presence of the
circularity guard, EN/ZH `H1` parity, EN/ZH figure-reference parity, and the
exporter determinism diff. Extend it when you add a deliverable — a check that
catches one real defect per run is worth more than a page of prose.

---

## 4. Pitfall ledger

Every one of these cost real time. Ordered roughly by how much.

| # | Symptom | Cause | Fix |
|---|---|---|---|
| P1 | `.git` directory vanished mid-command | `git rebase --root --exec …` reported `could not mark as interactive` | **Never `git rebase` in this environment.** Re-init + recommit, or `--amend`. Worktree files were unharmed. |
| P2 | `git push` → `CONNECT tunnel failed, response 502` | sandbox exports `http_proxy`/`https_proxy`; `curl` and `gh api` survive it, streaming POST does not | Clear the proxy **for the push only**: `http_proxy= https_proxy= HTTP_PROXY= HTTPS_PROXY= git push origin main` |
| P3 | `remote rejected … without 'workflow' scope` | looked like a token-permission problem | **False alarm.** Same token, proxy cleared → pushed fine, workflow file included. Diagnose the transport before the credentials. |
| P4 | `.sh` fails with `xxx\r: command not found` | CRLF in a shell script | `.gitattributes` pins `.sh/.py/.tcl` to LF, `.bat` to CRLF. Add it in commit one. |
| P5 | `gh release create --notes-file /tmp/x.md` fails | MSYS `/tmp` and the path Python sees are different places | Use a real Windows path, e.g. `C:/Users/Admin/relnotes.md` |
| P6 | `Add-Type` + `System.IO.Compression` blocked by policy | PowerShell security policy | Use `C:/Windows/System32/tar.exe -a -cf …` and verify with `tar -tf … \| wc -l` |
| P7 | Python cannot write to `/d/…` | MSYS path vs Windows path | Always pass `D:\\…` to Python |
| P8 | Cannot embed SVG in docx/pptx; `reportlab` renderPM fails | no raster backend | matplotlib re-draw (`svg2png.py`) — see §3.3 |
| P9 | Deck table cell overflows / footer overlaps panel | cell text too long; note y beyond panel | deck: compress to one line, keep full wording in the Markdown; panel/note ≤ 5.90 in |
| P10 | First H1 rendered twice in the .docx (24pt + 20pt) | `continue` before advancing the line index | advance `i` before `continue` |
| P11 | `git status -sb` shows `origin/main [gone]` | sandbox FS will not persist `refs/remotes` | Cosmetic. Verify remote state with `gh api` or the web UI, not the local line |
| P12 | SVG arrowheads render black | `context-stroke` unsupported by some renderers | use explicit stroke colours on the marker paths |

---

## 5. Definition of Done

- [ ] `reviews/` has all five reviews, written at the time, verdict one word each
- [ ] every phase has an artifact; every claim has a source or a stated assumption
- [ ] version pins present and consistent across all documents (CI enforces)
- [ ] `run_all.sh` exit-code contract intact; circularity guard present
- [ ] exporter determinism proven by a byte-diff, in CI
- [ ] EN and ZH have the same section count; figures referenced in both
- [ ] `selfcheck.py` passes locally **and** on GitHub Actions
- [ ] `.docx` / `.pptx` regenerated after the last Markdown edit; zero overflow
- [ ] release notes state the known gaps
- [ ] `.gitattributes` present from the first commit
- [ ] LICENSE has a real copyright holder (no `<COPYRIGHT HOLDER>` placeholder)

---

## 6. Adapting this to Tutorial No. 3

**Keep unchanged:** the invariant in §0, the ten-step order, the two-key contract,
the exit-code contract, the five-review audit trail, the self-check, `.gitattributes`.

**Replace:** the subject matter, the domain agents, the gate chain, the pins.

| Decision | Question to answer at S0 |
|---|---|
| Subject | What is the one thing a reader can do afterwards that they could not before? |
| Gate chain | Which tools act as the neutral referee, and what makes a run **VOID** for *this* subject? |
| Domain agents | Who holds physics authority, and what is the defer clause for them? |
| Starter payload | What is the smallest thing that runs and can fail loudly? |
| Deliverables | Which formats, and is Markdown still the single source? |

**First 90 minutes, concretely:**

1. `git init -b main`; add `.gitattributes` and `.gitignore`; commit empty skeleton.
2. Write `PLAN.md` — scope, out-of-scope, team topology, Definition of Done.
3. Run `/plan-ceo-review`; land `reviews/01-ceo-review.md` **before** any prose.
4. Run `/spec`; land `reviews/02-spec.md` with the W-tasks and the escalations.
5. Pin the toolchain; write `versions.lock.template`.
6. Copy `.github/scripts/selfcheck.py` and edit the required-file list.

Everything after that is S3–S9 on repeat.

---

*Licence: prose CC BY 4.0, code Apache-2.0 — Copyright 2026 Prof. Yi-Kuen Lee.*

# Review 05 — Ship (`/ship`)

> **Status: reference example.** The release checklist that actually shipped.

```
Date:            2026-09-01
Reviewer role:   DevOps
Command:         /ship
Scope reviewed:  release contents, bilingual parity, licence, limitation disclosure
Verdict:         PASS
```

---

## Release contents

| Item | Present | Notes |
|---|---|---|
| `VERSIONS.lock` | ✅ | all four tools pinned with commits |
| Gate logs — 5, 6, 7A, 7B-1R2 | ✅ | four separate files, append-only |
| GDS + `sha256.txt` | ✅ | from the frozen-timestamp run |
| `README.md` + `README.zh.md` | ✅ | parity checked (below) |
| Known limitations section | ✅ | mandatory, not optional |
| Licence | ✅ | prose CC BY 4.0, code Apache-2.0 |
| Tutorial in 3 formats × 2 languages | ✅ | md (source) + docx + pptx |

---

## Bilingual parity check

| Check | Result |
|---|---|
| Section counts (EN vs ZH) | equal |
| Every EN heading has a ZH counterpart | ✅ |
| Gate numbers identical across languages | ✅ |
| Version pins identical across languages | ✅ |
| No EN-only claim in the ZH doc | ✅ |

**Parity rule adopted:** a change that lands in one language and not the other fails
the release. The four-file rule from Tutorial #1 generalises here to
**1 conceptual change = 4 files × 4 checks** (EN doc, ZH doc, code/config, review record).

---

## Licence review

| Component | Licence | Clear to redistribute? |
|---|---|---|
| Tutorial prose | CC BY 4.0 | ✅ |
| Tutorial scripts / config templates | Apache-2.0 | ✅ |
| SkyWater SKY130A PDK | Apache-2.0 (open PDK) | ✅ — but **not vendored**; referenced by URL |
| Magic / Netgen / open_pdks / Microlane | OSS | ✅ — not vendored |
| TinyTapeout VM image | Apache-2.0 | ✅ — referenced, not vendored |
| `e2e-ic-system` commercial package | separately licensed | ❌ **not included**, explicitly stated |

---

## Limitation disclosure (verbatim from the release notes)

**In this release**
- Digital gate chain: DRC, extraction, structural LVS, hierarchical LVS
- Deterministic, byte-reproducible GDS
- Bilingual documentation

**On the roadmap (v1.1+)**
- PEX / RCX · post-layout simulation · full STA · IR drop / EM / antenna
- Gate 7B-2, device-level LVS
- A gate chain for the analog track

**Positioning (honest numbers)**
- Teaching / research objectives: **~70–85 % covered**
- Commercial sign-off: **~15–25 %** — budget for supplementary tools, or wait for v1.1

This is not a Cadence-grade sign-off flow and does not claim to be.

---

## The four-file rule — audit

| Change | EN doc | ZH doc | Code / config | Review record |
|---|---|---|---|---|
| Authority contract added (§0.4) | ✅ | ✅ | ✅ `docs/expertise_division{,.zh}.md` | ✅ `01` addendum |
| Circular-LVS → VOID | ✅ | ✅ | ✅ exit code 2 | ✅ `03` B4 |
| Two-baseline SHA policy | ✅ | ✅ | ✅ `VERSIONS.lock` template | ✅ `04` Q3 |
| Slide count 28 → 33 | ✅ | ✅ | ✅ `_build/` regenerated | ✅ this record |

---

## Blocking issues

**B7 — Deck page count stated as 28 in `README.md` while the deck has 33 slides.**
Stale documentation in a release is a defect, not a nitpick. *Fixed by:* regenerating
and correcting both READMEs; CI now checks the stated count against the built artifact.

---

## Non-blocking notes

- `dist/` binaries are generated. They are committed so a reader can use them without
  a Python toolchain, but the Markdown is the source of truth and hand-editing the
  binaries is prohibited.
- Recommend a `repo-selfcheck` CI job: required files present, version pins consistent
  across all documents, no untranslated EN-only headings.
- Consider a GitHub release asset per language rather than one zip containing both.

---

## Decisions recorded

| # | Decision |
|---|---|
| H1 | `dist/` is committed (convenience) **and** regenerable (integrity). Both, not either. |
| H2 | The commercial product is referenced, never bundled. |
| H3 | Every release restates the limitation table. Silence about limits reads as a claim. |
| H4 | Repo self-check runs on every push. |

---

## What was NOT reviewed

- Analog track technical content (no gate; review 04 lists it as unchecked).
- The correctness of the valuation appendix (CEO-owned; method published, inputs are
  the reader's to audit).

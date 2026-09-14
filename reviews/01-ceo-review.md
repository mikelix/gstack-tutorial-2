# Review 01 — CEO (`/plan-ceo-review`)

> **Status: reference example.** This is the author's own run, reproduced so you can
> see what a *good* CEO review looks like. Your numbers, your cut list and your open
> questions will be different. Do not copy the verdicts — copy the shape.

```
Date:            2026-08-21
Reviewer role:   owner / CEO
Command:         /plan-ceo-review
Scope reviewed:  project charter + claimed positioning (teaching platform, ~RMB 1.25M)
Verdict:         REVISE
```

---

## Blocking issues

**B1 — The valuation number is doing work it cannot do.**
The charter says "a system independently valued at ~RMB 1.25 M". No reader can
verify that, and an unverifiable number in the first paragraph makes everything
after it suspect.
*Fixed when:* the number is either (a) accompanied by the method and inputs that
produced it, or (b) removed from the headline and moved to an appendix with its
assumptions exposed.

**B2 — "End-to-end" is not currently true and the charter does not say so.**
PEX/RCX, post-layout simulation, full STA, IR/EM/antenna and device-level LVS
(Gate 7B-2) are not implemented. The charter implies a complete flow.
*Fixed when:* out-of-scope items are listed in the charter itself, not only in the
README, and the release says "v1.0 — digital gate chain" rather than "end-to-end".

**B3 — No drop-out analysis.**
The single largest failure mode of this project is not a wrong GDS; it is a student
who never gets the toolchain installed. The charter has no plan for that.
*Fixed when:* at least two install paths are documented with honest time estimates,
and the recommended path is the one with the lowest drop-out rate (the VM image).

---

## Non-blocking notes

- The three-layer framing (orchestration / domain agents / tools+PDK) is the right
  abstraction and should be the spine of every document that follows.
- Bilingual from day one is correct. Retrofitting a Chinese version costs more than
  writing both.
- "Open PDK because the others are under NDA" is a *feature*, not an apology. Put it
  in the README as a worked example of an engineering-ethics decision.

---

## Decisions accepted

| # | Decision | Reason |
|---|---|---|
| D1 | Scope = **RTL → GDS + 4-gate verification + determinism proof**. Nothing else in v1.0. | Everything else is a v1.1 conversation. |
| D2 | PDK = **SkyWater SKY130A** exclusively. No NDA PDK content in the repo, ever. | Legal, and the rule decks are open so every gate is auditable. |
| D3 | Ship **bilingual** (EN + 简体中文). Markdown is the source of truth; Word/PPTX are generated. | One conceptual change = 4 files; make the generation mechanical. |
| D4 | Two domain agents are **mandatory**, not optional decoration. | See below (D5). |
| D5 | **Two-key authority**: process decisions to gstack, physics/flow decisions to the domain agents; on conflict, physics wins. | The gstack roles are process experts and domain generalists. They will accept `LVS passed` without knowing the check can be circular. |

---

## Decisions rejected (with reason)

| # | Rejected proposal | Why |
|---|---|---|
| R1 | "Relax the DRC deck to reach zero violations." | A gate that is relaxed to pass is not a gate. Fix the layout. |
| R2 | "Add PEX/RCX so we can say *end-to-end*." | Ships a half-implemented check and calls it verification. Roadmap item, clearly labelled. |
| R3 | "Let the AI PM own the gate definitions." | Gate definitions are domain semantics. PM owns decomposition, not physics. |
| R4 | "Show the ams 0.35 µm PDK to prove industry experience." | NDA. Non-negotiable. Credibility comes from the method, not from exhibiting someone else's property. |

---

## Scope cut list (cut in this order when time runs short)

1. Analog agent track (Part 9) — it has no gate chain yet; it is enrichment, not proof.
2. Assessment material (Part 11) — only needed if this is taught as a course.
3. The PPTX/Word deliverables — Markdown is enough to *use* the tutorial.
4. **Never cut:** Gates 5 / 6 / 7A / 7B-1R2, the determinism proof, or the
   non-circular reference export. Cut those and the tutorial has no intellectual content.

---

## Open questions (deliberately unanswered at this stage)

1. What is the reference GDS SHA on the TinyTapeout VM chain? Unknown until a VM run
   completes. Expect it to differ from the Windows/Cygwin baseline.
2. Can Gate 7B-2 (device-level LVS) be closed with the rule decks already in the PDK,
   or does it need new work? **Referred to AI GDS-Architect — not answerable by this role.**
3. Does the analog track need a gate chain at all, or is simulation + human review the
   honest answer for v1.0? **Referred to Senior Analog IC Architect.**

> Note questions 2 and 3. They are marked **referred**, not answered. That is the
> defer clause working: this role identified the questions and refused to guess.

---

## What was NOT reviewed

- Any tool version or install script (no environment existed yet).
- The analog track in any depth.
- Licence compatibility of the VM image's bundled OpenLane (checked later, Apache-2.0).

---

## Addendum

**2026-09-14 — after the run completed.**
B1 resolved by publishing the valuation method and its assumptions in an appendix and
moving the number out of the headline claim. B2 resolved by renaming the release
"digital gate chain v1.0" and listing 7B-2 / PEX / STA as roadmap. B3 resolved by
promoting the VM path (Option C) to *recommended* and adding the cloud-build variant
for students without 20 GB of local disk. Verdict upgraded to **PASS**.

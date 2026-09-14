# -*- coding: utf-8 -*-
"""English deck: gstack Tutorial No. 2"""
import sys
sys.path.insert(0, r'D:\ipason\EDA\gstack-tutorial-2\_build')
from deck import *  # noqa
from deck import NAVY, NAVY2, ACCENT, ACCENT2, WHITE, LIGHT, GREY, DARK

FOOT = "gstack Tutorial No. 2  ·  Build an AI-Agent End-to-End EDA System on WorkBuddy"


def build_en(prs):
    n = [0]

    def num(s, dark=False):
        n[0] += 1
        footer(s, FOOT, dark)
        pagenum(s, n[0], dark)

    # 1 title
    num(slide_title(
        prs,
        "gstack TUTORIAL No. 2",
        "Build an AI-Agent End-to-End EDA System\non WorkBuddy",
        ["A step-by-step course for postgraduate students and junior engineers",
         "RTL → GDS on SkyWater SKY130, verified by a four-gate chain and a byte-level hash"],
        "Version 1.0 · September 2026 · Prose CC BY 4.0 · Code Apache-2.0"), dark=True)

    # 2 what you build
    num(slide_bullets(
        prs,
        "What you will build — and what you must prove",
        ["Build an open-source RTL → GDS flow on the SkyWater SKY130 open PDK",
         "Drive it with 5 gstack orchestration roles plus 2 domain AI agents",
         "Prove it with four verification gates and a reproducible SHA-256",
         "Ship it with bilingual documentation and an honest limitations section"],
        note="You do not need a commercial EDA licence, an NDA, or a tape-out budget."))

    # 3 why a second tutorial
    num(slide_table(
        prs,
        "Why a second tutorial?",
        ["", "Tutorial #1", "Tutorial #2"],
        [["Carrier", "hello_world.py", "a real RTL→GDS EDA system"],
         ["Team", "5 gstack review roles", "5 gstack roles × 2 domain agents"],
         ["Proof of done", "review notes merged", "gate chain PASS + GDS SHA match"],
         ["Environment", "none", "reproducible open EDA + open PDK"],
         ["Value narrative", "—", "a system valued at ~RMB 1.25 M"]],
        col_widths=[1.5, 3.0, 4.2], first_bold=True,
        note="Tutorial #1 deliberately carries no real artifact. That was the right choice — until you need one."))

    # 4 three-layer model
    num(slide_layers(
        prs,
        "The three-layer model",
        [("Layer 1\ngstack orchestration",
          ["/plan-ceo-review → /spec → /plan-eng-review → /qa-only → /ship",
           "Each role has a stop point, so decisions get audited — not absorbed."], NAVY),
         ("Layer 2\ntwo domain agents",
          ["AI GDS-Architect — digital: RTL→GDS, DRC, LVS, determinism",
           "Senior Analog IC Architect — analog: sizing, simulation, layout intent",
           "Each has a handoff contract: what it receives, produces, is judged by."], ACCENT),
         ("Layer 3\nopen EDA + PDK + gates",
          ["Magic 8.3.681 · Netgen 1.5.323 · KLayout · ngspice · Xschem",
           "SKY130A (open_pdks 1.0.572) · Microlane P&R",
           "Gate 5 DRC → Gate 6 Extraction → Gate 7A LVS → Gate 7B-1R2 LVS"], NAVY2)],
        note="An agent whose output no gate examines is doing homework, not engineering."))

    # 5 five roles
    num(slide_table(
        prs,
        "The five gstack roles",
        ["Command", "Role", "Job", "Stops when"],
        [["/plan-ceo-review", "AI CEO", "Challenge scope, positioning, ambition", "scope is defensible"],
         ["/spec", "AI PM", "Decompose into assignable work items", "backlog is concrete"],
         ["/plan-eng-review", "AI Engineer", "Lock architecture, data flow, order", "plan is buildable"],
         ["/qa-only", "AI QC", "Test and report — without fixing", "report is filed"],
         ["/ship", "AI DevOps", "Version, package, document, release", "release is tagged"]],
        col_widths=[1.7, 1.1, 3.6, 2.0], first_bold=True,
        note="The value is not that the AI is clever. It is that every role has a stop point."))

    # 6 two agents
    num(slide_table(
        prs,
        "The two domain agents",
        ["Agent", "Owns", "Produces", "Judged by"],
        [["AI GDS-Architect",
          "Digital backend: P&R, DRC, extraction, LVS, stream-out",
          "GDS, extracted netlist, gate logs",
          "Gates 5, 6, 7A, 7B-1R2"],
         ["Senior Analog IC Architect",
          "Analog front-end: topology, sizing, simulation",
          "Sized schematic, sim results, layout constraints",
          "ngspice sim, DRC, (7B-2 on roadmap)"]],
        col_widths=[1.7, 3.0, 2.4, 1.9], first_bold=True, size=11.5,
        note="The digital agent carries the main line. The analog agent joins at Part 9."))

    # 6b the expertise gap
    num(slide_table(
        prs,
        "The expertise gap — why five roles are not enough",
        ["A gstack role will happily…", "…but it does not know that"],
        [["accept \"LVS passed\"", "a naive LVS can be circular and prove nothing"],
         ["accept \"DRC clean\"", "which rule classes actually ran, and what was waived"],
         ["reorder build steps for tidiness", "stream order changes the GDS byte stream and breaks determinism"],
         ["suggest \"relax the check to get green\"", "relaxing a sign-off check is the one unforgivable move"],
         ["package whatever exists", "a GDS without a reproducible hash is not a release"],
         ["draft the positioning text", "one wrong physics number destroys the whole credibility"]],
        col_widths=[5.6, 5.6], first_bold=True, size=11.5,
        kicker="THE SECOND, MORE IMPORTANT DIFFERENCE FROM TUTORIAL #1",
        note="gstack roles are process experts and domain generalists by design. That is what makes them good orchestrators."))

    # 6c two-key system
    num(slide_quote(
        prs,
        "Process authority sits with gstack.\nPhysics authority sits with the domain agents.\nOn conflict, physics wins.",
        "Not \"5 + 2\". A two-key system — 5 who decide process, 2 who decide physics.",
        "THE TWO-KEY SYSTEM"))

    # 6d authority contract
    num(slide_table(
        prs,
        "The authority contract — who decides what",
        ["Decision", "gstack", "Domain agent", "Human"],
        [["Scope, phasing, work breakdown", "decides", "consulted", "approves"],
         ["PDK / stdcell library choice", "—", "DECIDES", "approves"],
         ["What counts as a passing gate", "runs it", "DECIDES", "—"],
         ["Waiver of a DRC violation", "not allowed", "DECIDES", "signs"],
         ["Interpretation of an LVS mismatch", "reports", "DECIDES", "—"],
         ["Release content and version", "decides", "consulted", "approves"],
         ["Any statement with a physics number", "not allowed", "DECIDES", "—"]],
        col_widths=[4.4, 2.3, 2.7, 1.8], first_bold=True, size=11.5,
        note="Read the \"not allowed\" rows first. They are the point of the table."))

    # 6e veto rules
    num(slide_bullets(
        prs,
        "Three veto rules",
        ["Domain veto beats process convenience — an unsafe step does not happen, whatever the plan says",
         "A gate result is not a fact until the domain agent has read the log, not just the status line",
         "No check is ever relaxed to make a build pass — the domain agent states which is wrong, in writing"],
        kicker="THE CONTRACT",
        note="\"PASS\" is a string. The log is the evidence."))

    # 6f defer clause
    num(slide_code(
        prs,
        "The defer clause — paste into every gstack prompt",
        ["CONSULT REQUIRED. Before you finalise any statement about DRC, LVS,",
         "extraction, determinism, or PDK rules, hand that specific claim to",
         "the domain agent (AI GDS-Architect for digital, Senior Analog IC",
         "Architect for analog) and quote its answer verbatim.",
         "",
         "If the domain agent contradicts you, the domain agent wins. Do not",
         "resolve the conflict yourself - escalate to the human with both",
         "statements side by side."],
        lang_note="One paragraph. It is the difference between sounding right and being right.",
        note="Why the agents are credible: non-circular LVS, deterministic GDS, and a 22-year chain from a Lyapunov exponent (2002) to a certified diagnostic (2023)."))

    # 7 why sky130
    num(slide_bullets(
        prs,
        "Why SKY130, not a commercial PDK",
        ["An NDA PDK cannot be published, redistributed or committed",
         "An \"open-source tutorial\" shipping a closed PDK is not open source — it is a leak with a README",
         "SKY130 is the first foundry-grade PDK under an open licence, with open DRC/LVS/RCX rule decks",
         "Nothing is lost: the method is process-agnostic and transfers to any PDK"],
        note="This section is itself the lesson: it teaches what may be open-sourced, using a real decision."))

    # 8 course map
    num(slide_table(
        prs,
        "Course map",
        ["Part", "What you do", "Time"],
        [["0", "Mental model: three layers, five roles, two agents", "30 min"],
         ["1", "Install WorkBuddy, gstack and the two domain agents", "45 min"],
         ["2", "Install the open EDA toolchain (three paths)", "30 min – 4 h"],
         ["3", "Phase 1 — AI CEO sets the scope", "45 min"],
         ["4", "Phase 2 — AI PM decomposes the work", "45 min"],
         ["5", "Phase 3 — AI Engineer runs RTL → GDS", "3–5 h"],
         ["6", "Phase 4 — AI QC verifies and proves determinism", "2–3 h"],
         ["7", "Phase 5 — AI DevOps ships it", "1–2 h"],
         ["8", "The two disciplines this tutorial actually teaches", "30 min"],
         ["9", "Bring in the analog agent", "2–4 h"],
         ["10–12", "Troubleshooting, assessment, where to go next", "self-paced"]],
        col_widths=[0.9, 7.5, 1.6], first_bold=True, size=12,
        note="Total: 10–14 h for a first pass. Every part ends with a checkpoint you must pass."))

    # 9 part 0 checkpoint
    num(slide_checklist(
        prs,
        "Part 0 — Checkpoint",
        ["You can name all five gstack commands and each one's stop point",
         "You can state, in one sentence, the difference between Tutorial #1 and #2",
         "You can explain why an NDA PDK cannot appear in this repository",
         "You can name one decision the gstack roles may NOT make, and who makes it",
         "You have the defer clause copied where you can paste it from"],
        note="Do not advance until all five are green. The mental model is the transferable part."))

    # 10 part 1 steps
    num(slide_steps(
        prs,
        "Part 1 — Install the host and the two agents",
        ["Download Tencent WorkBuddy, install, sign in, verify with a trivial prompt",
         "Install the gstack skill suite; confirm @skill:gstack routes to the right skill",
         "Create ~/.workbuddy/skills/e2e-ic-system/agents/",
         "Save ai_gds_architect.md and analog_ic_architect.md (minimal briefs are in Part 1.3)",
         "Restart WorkBuddy and confirm: \"List the agents you can see\""],
        note="Agent specs are host-agnostic — Claude Code and OpenAI Codex work the same way."))

    # 11 install paths
    num(slide_table(
        prs,
        "Part 2 — Three install paths",
        ["Path", "Platform", "Time", "Status"],
        [["A — one-click installer (install_eda.bat)", "Windows 11", "1–3 h (compiles)", "beta"],
         ["B — manual step-by-step", "any", "2–4 h", "fully documented"],
         ["C — TinyTapeout VM image (recommended)", "Win / macOS / Linux", "~30 min", "upstream-maintained"]],
        col_widths=[4.0, 2.2, 1.9, 2.2], first_bold=True, size=11.5,
        note="If you have never installed an open EDA toolchain, take Option C. Do not spend day one compiling."))

    # 12 pinned versions
    num(slide_table(
        prs,
        "Pinned versions — do not drift",
        ["Component", "Version", "Commit", "Source"],
        [["Magic", "8.3.681", "4432d7e", "RTimothyEdwards/magic"],
         ["Netgen", "1.5.323", "bb8a610", "RTimothyEdwards/netgen"],
         ["open_pdks / SKY130A", "1.0.572", "54435919", "RTimothyEdwards/open_pdks"],
         ["Microlane", "—", "87079e7f6", "htfab/microlane"]],
        col_widths=[2.6, 1.7, 1.7, 4.3], first_bold=True,
        note="Version drift is the single most common cause of a mysterious SHA mismatch."))

    # 13 verify
    num(slide_code(
        prs,
        "Verify before you go further",
        ["magic   -dnull -noconsole --version",
         "netgen  -batch -nogui",
         "cat $PDK_ROOT/sky130A/.config/nodeinfo.json",
         "ls $PDK_ROOT/sky130A/libs.tech",
         "",
         "# expected:",
         "#   node sky130A · 130 nm · open_pdks 1.0.572 (54435919)",
         "#   magic 8.3.681 (4432d7e) · 11 stdcell libs",
         "#   sky130_fd_sc_hd: 446 cells"],
        lang_note="If all four respond, you are ready for Phase 1.",
        note="The open PDK ships DRC, LVS and RCX rule decks — the PEX gap is in our pipeline, not the PDK."))

    # 14 phase 1 CEO
    num(slide_bullets(
        prs,
        "Phase 1 — AI CEO sets the scope",
        ["Run /plan-ceo-review and paste your scope statement",
         "Ask explicitly: what should I cut first? Which claim is weakest?",
         "A good review returns four things — risk-ranked scope, a cut list, a challenge, an open question",
         "Write the outcome into reviews/01-ceo-review.md"],
        kicker="PHASE 1 · /plan-ceo-review · 45 MIN",
        note="If the review raises no question you cannot answer yet, the review is shallow."))

    # 15 phase 2 WBS
    num(slide_table(
        prs,
        "Phase 2 — Work breakdown",
        ["ID", "Work item", "Owner", "Judged by"],
        [["W1", "Toolchain install + VERSIONS.lock", "DevOps", "Checkpoint 2"],
         ["W2", "Agent install + handoff contract", "DevOps", "Checkpoint 1"],
         ["W3", "config.env + isolated launcher", "Engineer", "launcher runs"],
         ["W4", "Place-and-route to GDS", "AI GDS-Architect", "Gates 5, 6"],
         ["W5", "Non-circular reference source export", "AI GDS-Architect", "artifact not GDS-derived"],
         ["W6", "LVS pair (7A, 7B-1R2)", "AI GDS-Architect", "Gates 7A, 7B-1R2"],
         ["W7", "Determinism proof (repeat run, compare SHA)", "QC", "SHA identical"],
         ["W8", "Analog sizing + simulation (optional track)", "Analog IC Architect", "ngspice sim"],
         ["W9", "Bilingual docs + release package", "DevOps", "Definition of Done"]],
        col_widths=[0.6, 4.4, 2.6, 2.7], first_bold=True, size=11.5,
        note="Every work item names the gate that judges it. No gate, no credit."))

    # 16 phase 3
    num(slide_bullets(
        prs,
        "Phase 3 — AI Engineer runs RTL → GDS",
        ["Run /plan-eng-review first: lock data flow, artifact naming, gate positions",
         "Ask the question juniors never ask: what happens to the run directory when a gate fails?",
         "Dispatch the AI GDS-Architect with the four mandatory report lines",
         "Use the isolated launcher — never a bare shell on Windows"],
        kicker="PHASE 3 · /plan-eng-review · 3–5 H",
        note="Mandatory report lines: artifacts with paths · gate status · GDS sha256 · what was NOT checked."))

    # 17 non-circularity
    num(slide_flow(
        prs,
        "The non-circularity rule — the intellectual core",
        [(0.62, 2.20, 2.6, 0.95, "P&R database\n(live)", NAVY, True),
         (4.05, 1.75, 3.3, 0.72, "db_source_export.py\n(pre stream-out)", ACCENT, True),
         (4.05, 2.90, 3.3, 0.72, "GDS → Magic extract", NAVY2, True),
         (8.20, 1.75, 3.3, 0.72, "reference source", ACCENT, False),
         (8.20, 2.90, 3.3, 0.72, "layout netlist", NAVY2, False),
         (4.05, 4.15, 7.45, 0.80, "Netgen hierarchical LVS  →  Gate 7B-1R2", NAVY, True),
         (0.62, 5.30, 12.1, 0.62,
          "Comparing a GDS netlist against the same GDS always passes. Two derivations from one live database do not.",
          LIGHT, False)],
        note="Decap power/ground must come from the authoritative PDK CDL/SPICE, not from the layout."))

    # 18 four gates
    num(slide_table(
        prs,
        "The four gates",
        ["Gate", "Checks", "Tool", "Pass criterion"],
        [["5 — DRC", "geometry vs foundry rules", "Magic 8.3.681", "0 violations (waivers listed)"],
         ["6 — Extraction", "layout → netlist", "Magic 8.3.681", "completes; warnings enumerated"],
         ["7A — Structural LVS", "P&R netlist vs gate-level netlist", "Microlane comparator", "structural match"],
         ["7B-1R2 — Hier. LVS", "extracted vs P&R-DB-derived source", "Netgen 1.5.323", "Circuits match uniquely."]],
        col_widths=[2.0, 3.4, 2.3, 3.4], first_bold=True, size=11.5,
        note="A gate with no artifact did not run."))

    # 18b exit-code contract
    num(slide_table(
        prs,
        "The exit-code contract — VOID gets its own code",
        ["Code", "Meaning", "What you must do"],
        [["0", "all gates PASS", "record the SHA and move on"],
         ["1", "a gate FAILED", "freeze the run dir, read the log, fix the cause"],
         ["2", "a gate returned VOID", "the check proved nothing — re-derive the reference, re-run"],
         ["3", "environment error", "bad config, missing tool, or a reused RUN_DIR"]],
        col_widths=[0.9, 4.0, 6.3], first_bold=True, size=12,
        note="If VOID shared a code with PASS, a reviewer skimming — or a CI job asserting only \"non-zero\" — could mistake it for success."))

    # 19 phase 4
    num(slide_bullets(
        prs,
        "Phase 4 — AI QC verifies, and you prove determinism",
        ["Organisational rule: the person who ran a gate cannot certify it",
         "Run /qa-only — it reports, it does not fix",
         "Run the whole chain twice in clean shells and compare sha256 of the GDS",
         "Record everything in VERSIONS.lock; publish two baselines (Windows chain, VM chain)"],
        kicker="PHASE 4 · /qa-only · 2–3 H",
        note="Do not \"fix\" a SHA mismatch by relaxing the check. Investigate it."))

    # 20 phase 5
    num(slide_two_col(
        prs,
        "Phase 5 — AI DevOps ships it",
        "Release must contain",
        ["VERSIONS.lock — reproducibility",
         "Gate logs for all four gates",
         "GDS + reference SHA",
         "README (EN) + README (ZH)",
         "Known limitations section",
         "Licence: CC BY 4.0 prose, Apache-2.0 code"],
        "The four-file rule",
        ["One conceptual change = 4 files × 4 checks",
         "Gate script · EN doc · ZH doc · review record",
         "Each must be re-checked",
         "Budget for it at the start",
         "Do not discover it at the end"],
        kicker="PHASE 5 · /ship · 1–2 H",
        note="Carried over verbatim from Tutorial #1, because it is still true."))

    # 21 discipline 1
    num(slide_bullets(
        prs,
        "Discipline 1 — Lock the artifact",
        ["Pinned tool versions + PYTHONHASHSEED=0 + seeded RNG + frozen GDS timestamp",
         "⇒ byte-identical output ⇒ a hash you can publish",
         "An AI agent can produce something plausible in minutes",
         "The only thing between \"plausible\" and \"engineering\" is a referee that cannot be argued with"],
        kicker="WHAT THIS TUTORIAL ACTUALLY TEACHES",
        note="A hash is such a referee."))

    # 22 discipline 2
    num(slide_table(
        prs,
        "Discipline 2 — Check the number, not just the status",
        ["Case", "Predicted", "Measured", "Error"],
        [["Quadcopter hover power (GDA)", "127.8 W", "127.4 W", "0.29 %"],
         ["CTC capture critical capillary number Ca*", "0.043", "0.04 ± 0.006", "inside band"]],
        col_widths=[4.6, 2.0, 2.4, 2.3], first_bold=True, size=12.5,
        note="Both survive a first-principles cross-check — and both state their falsifiable assumption openly."))

    # 23 the sentence
    num(slide_quote(
        prs,
        "\"FM = 0.39, taken independently from propeller data — not fitted to this flight.\"",
        "Volunteering the assumption under which your number could be wrong is what converts a claim into evidence.",
        "THE SENTENCE THAT MATTERS"))

    # 24 analog agent
    num(slide_bullets(
        prs,
        "Part 9 — Bringing in the analog agent",
        ["Senior Analog IC Architect owns: schematic, sizing, simulation, corners, layout intent",
         "Tools: Xschem → ngspice → Magic",
         "Always ask it to name the one assumption most likely to be wrong",
         "Honest status: its gates are not yet implemented — judged by simulation and human review"],
        kicker="PART 9 · 2–4 H",
        note="22 years from a Lyapunov exponent to a certified diagnostic. The domain changed; the discipline did not."))

    # 25 troubleshooting
    num(slide_table(
        prs,
        "Troubleshooting — top six",
        ["Symptom", "Likely cause", "Fix"],
        [["magic: command not found", "not on PATH / Cygwin not isolated", "use the launcher; check config.env"],
         ["SHA differs between runs", "version drift, timestamp not frozen", "VERSIONS.lock; PYTHONHASHSEED=0"],
         ["SHA differs on the VM", "different PDK build and tool revisions", "expected — publish a second baseline"],
         ["Netgen setup-file error", "6-arg form used in a sourced script", "use the 4-arg Tcl form"],
         ["Paths look corrupted", "MSYS path mangling", "env -i + MSYS2_ARG_CONV_EXCL='*'"],
         ["LVS passes suspiciously easily", "circular comparison (GDS vs GDS)", "reference must come from the P&R DB"]],
        col_widths=[3.4, 4.1, 4.6], first_bold=True, size=11))

    # 26 assessment
    num(slide_table(
        prs,
        "Assessment — grading rubric",
        ["Criterion", "Weight"],
        [["All four gates PASS with artifacts", "30 %"],
         ["SHA reproducible and recorded", "20 %"],
         ["Limitations stated honestly and specifically", "20 %"],
         ["Discipline 2 demonstrated — a number recomputed by hand", "20 %"],
         ["Bilingual or clearly documented output", "10 %"]],
        col_widths=[8.5, 2.0], first_bold=True, size=13,
        note="Labs: reproduce · break it deliberately · circular LVS · physics vs status · agent accountability."))

    # 27 next
    num(slide_bullets(
        prs,
        "Where to go next",
        ["PEX / RCX and Gate 7B-2 — the rule decks already ship with the PDK",
         "Post-layout simulation with ngspice; full STA via OpenLane/OpenSTA (needs Docker)",
         "Tape-out through the TinyTapeout shuttle, from $100",
         "Give the analog agent a real gate chain — high effort, high value"],
        note="Credits: google/skywater-pdk · open_pdks · Magic · Netgen · Microlane · Tiny Tapeout · Zero to ASIC · SiliWiz"))

    # 27b what ships in the repo
    num(slide_two_col(
        prs,
        "What ships in the repository",
        "Runnable skeleton — starter/",
        ["run_all.sh drives all four gates + circularity guard + fingerprint",
         "run_drc.tcl · run_extract.tcl · run_lvs.tcl",
         "db_export.py — the pre-streamout reference export",
         "config.env.example · versions.lock.template · designs/"],
        "Audit trail — reviews/",
        ["01 CEO — scope, cut list, questions referred not guessed",
         "02 spec — W1–W9, critical path, three escalations",
         "03 eng — the circular LVS found VOID, then fixed",
         "04 QA — and an eight-row \"what was NOT checked\" table",
         "05 ship — contents, parity, licences, four-file audit"],
        note="CI (.github/workflows/selfcheck.yml) fails if a version pin drifts between documents, or if the circularity guard disappears."))

    # 28 close
    num(slide_quote(
        prs,
        "In #1 the agents review the work.\nIn #2 the agents do the work —\nand are held to a verification gate.",
        "Your tutorial is complete when your four gates pass and your SHA reproduces.",
        "THE ONE-LINE DIFFERENCE"), dark=True)


if __name__ == '__main__':
    build(r'D:\ipason\EDA\gstack-tutorial-2\dist\gstack-tutorial-2_EN.pptx', build_en)

#!/usr/bin/env python3
"""repo self-check — the checks that must pass on every push.

Purpose: stop the two failure modes this project is actually prone to.

  1. DRIFT   — a version pin updated in one document and not in the others.
               Four documents carry the same pins; a mismatch means some reader
               is being told the wrong thing.
  2. SILENCE — the circularity guard quietly disappearing from run_all.sh, or a
               review record being deleted. The audit trail is the product; if
               it erodes, the tutorial is no longer teaching what it claims.

Exit: 0 pass, 1 fail. No third state — this checker has no VOID, because a
self-check that can return "unknown" is a self-check people learn to ignore.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

PINS = {
    "magic":     "8.3.681",
    "netgen":    "1.5.323",
    "open_pdks": "1.0.572",
}
PIN_DOCS = [
    "README.md",
    "README.zh.md",
    "PLAN.md",
    "TUTORIAL.md",
    "TUTORIAL.zh.md",
    "starter/versions.lock.template",
]

REQUIRED = [
    "README.md",
    "README.zh.md",
    "TUTORIAL.md",
    "TUTORIAL.zh.md",
    "PLAN.md",
    "START_HERE.md",
    "COLLABORATOR_GUIDE.md",
    "LICENSE.md",
    "docs/gate_chain.md",
    "docs/expertise_division.md",
    "docs/expertise_division.zh.md",
    "docs/two-key-authority.svg",
    "docs/two-key-authority.png",
    "reviews/README.md",
    "reviews/01-ceo-review.md",
    "reviews/02-spec.md",
    "reviews/03-eng-review.md",
    "reviews/04-qa-report.md",
    "reviews/05-ship.md",
    "starter/README.md",
    "starter/config.env.example",
    "starter/versions.lock.template",
    "starter/scripts/run_all.sh",
    "starter/scripts/run_drc.tcl",
    "starter/scripts/run_extract.tcl",
    "starter/scripts/run_lvs.tcl",
    "starter/scripts/db_export.py",
    "starter/designs/my_first_gds.v",
    "starter/designs/layout.db.json",
]

# The guard that makes VOID detectable rather than a matter of luck.
CIRCULARITY_GUARD = "db_export_marker"

errors: list[str] = []
warnings: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def check_required() -> None:
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            fail(f"missing required file: {rel}")


def check_pins() -> None:
    for rel in PIN_DOCS:
        p = ROOT / rel
        if not p.is_file():
            continue  # already reported by check_required
        text = p.read_text(encoding="utf-8")
        for name, ver in PINS.items():
            if ver not in text:
                fail(f"{rel}: pin '{name} {ver}' not found")


def check_circularity_guard() -> None:
    p = ROOT / "starter/scripts/run_all.sh"
    if not p.is_file():
        return
    text = p.read_text(encoding="utf-8")
    if CIRCULARITY_GUARD not in text:
        fail(
            "starter/scripts/run_all.sh: circularity guard missing "
            f"('{CIRCULARITY_GUARD}'). Gate 7B-1R2 would be able to pass "
            "circularly without detection."
        )
    if "die 2" not in text:
        fail(
            "starter/scripts/run_all.sh: no VOID exit path ('die 2'). VOID must "
            "have its own exit code so it cannot be mistaken for success."
        )


def check_bilingual_parity() -> None:
    en = ROOT / "TUTORIAL.md"
    zh = ROOT / "TUTORIAL.zh.md"
    if not (en.is_file() and zh.is_file()):
        return
    en_t = en.read_text(encoding="utf-8")
    zh_t = zh.read_text(encoding="utf-8")
    h1_en = len(re.findall(r"^# ", en_t, re.M))
    h1_zh = len(re.findall(r"^# ", zh_t, re.M))
    if h1_en != h1_zh:
        warn(
            f"bilingual parity: {h1_en} top-level sections in EN vs {h1_zh} in ZH "
            "— a section may not have been translated"
        )
    fig_en = en_t.count("two-key-authority")
    fig_zh = zh_t.count("two-key-authority")
    if fig_en == 0 or fig_zh == 0:
        fail("the two-key authority figure is not referenced in both tutorials")
    elif fig_en != fig_zh:
        warn(f"bilingual parity: figure referenced {fig_en}x in EN vs {fig_zh}x in ZH")


def check_dist_freshness() -> None:
    src = ROOT / "TUTORIAL.md"
    dist = ROOT / "dist"
    if not src.is_file() or not dist.is_dir():
        return
    built = sorted(dist.glob("*.docx")) + sorted(dist.glob("*.pptx"))
    if not built:
        warn("dist/ has no generated .docx/.pptx — run the _build/ scripts")
        return
    src_m = src.stat().st_mtime
    stale = [b.name for b in built if b.stat().st_mtime < src_m]
    if stale:
        warn(
            "dist artifacts older than TUTORIAL.md: "
            + ", ".join(stale)
            + " — regenerate via _build/ (markdown is the source of truth)"
        )


def main() -> int:
    check_required()
    check_pins()
    check_circularity_guard()
    check_bilingual_parity()
    check_dist_freshness()

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")

    if errors:
        print(f"\nself-check FAILED — {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1

    print(f"self-check PASSED — {len(REQUIRED)} files, {len(PINS)} pins, "
          f"circularity guard present ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

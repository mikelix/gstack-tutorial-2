# reviews/

One file per gstack review. Written **at the time**, not reconstructed later —
the audit trail is the point.

| File | Command | Written by |
|---|---|---|
| `01-ceo-review.md` | `/plan-ceo-review` | owner |
| `02-spec.md` | `/spec` | PM |
| `03-eng-review.md` | `/plan-eng-review` | engineer |
| `04-qa-report.md` | `/qa-only` | QA |
| `05-ship.md` | `/ship` | DevOps |

## Format

```
Date:
Reviewer role:
Command:
Scope reviewed:

Verdict: PASS | REVISE | BLOCKED
Blocking issues:    (must be fixed before proceeding)
Non-blocking notes:
Decisions recorded: (so the next phase does not relitigate them)
```

## Rules

- **Verdict is one word.** PASS, REVISE, or BLOCKED. No hedging.
- **Blocking issues are specific** — file, line, what is wrong, what "fixed" means.
- **Every claim needs a source or a derivation.** No unsourced numbers.
- Reviews are **append-only**. Do not rewrite history; add a dated addendum.

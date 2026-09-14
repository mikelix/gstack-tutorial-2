# Publishing this repository to GitHub

## Status: PUBLISHED ✅

| Item | Value |
|---|---|
| Repo | <https://github.com/mikelix/gstack-tutorial-2> |
| Visibility | public |
| Branch | `main` |
| Commit | `db12056` — 42 files |
| CI | `repo self-check` green on first push — [run 34898901408](https://github.com/mikelix/gstack-tutorial-2/actions/runs/34898901408) |
| Licence | prose CC BY 4.0 · code Apache-2.0 · `Copyright 2026 Prof. Yi-Kuen Lee` |
| Topics | `ai-agents` `eda` `gstack` `magic` `netgen` `open-source-silicon` `rtl-to-gds` `sky130` `tutorial` `workbuddy` |

---

## `db12056` is not a code you can type anywhere

It is the **git commit hash** — the 7-hex-character short SHA of the single commit in
this repo. It appears in `git log --oneline`. GitHub's device-activation page asks for
a **device code**, which looks like `XXXX-XXXX` (8 characters, letter-digit mix, one
hyphen in the middle) and is printed by `gh auth login --web`. Two different things.

If you ever need to see the commit hash again:

```bash
git log --oneline          # db12056 gstack Tutorial No. 2 v1.0 ...
```

---

## The one thing that actually blocked the push

Not the token. Not the `workflow` scope (it turned out to be fine). It was the
**local HTTP proxy**:

```
fatal: unable to access 'https://github.com/...': CONNECT tunnel failed, response 502
```

This machine exports `http_proxy` / `https_proxy` → `http://127.0.0.1:50572`
(a WorkBuddy sandbox proxy). `curl` and `gh api` go through it happily;
`git push` — a large streaming POST — gets a 502 from the tunnel.

**Fix — clear the proxy for the push only:**

```bash
http_proxy= https_proxy= HTTP_PROXY= HTTPS_PROXY= git push -u origin main
```

Ten seconds, done. If a future push 502s again, this is the reason.

---

## How it was published (for the record)

1. `winget install --id GitHub.cli --exact` → `C:\Program Files\GitHub CLI\gh.exe` (v2.100.0)
2. `gh auth login --web --hostname github.com --git-protocol https --skip-ssh-key`
   → browser device activation at <https://github.com/login/device>
3. `gh repo create gstack-tutorial-2 --public --source=. --remote=origin --push`
4. Push retried with proxy cleared (see above)
5. `gh repo edit --add-topic …` and the Actions tab verified green

---

## Options if you need to redo this on another machine

### A — GitHub Desktop (`app-3.6.3`, installed)

1. **File → Add local repository…** → `D:\ipason\EDA\gstack-tutorial-2`
2. **Add repository**
3. Top bar → **Publish repository**
4. Name `gstack-tutorial-2`, **uncheck** "Keep this code private" → **Publish repository**

Desktop's OAuth token already carries the `workflow` scope.

### B — command line

Git Credential Manager is installed (`credential.helper = helper-selector`), so the
first push opens a browser OAuth — no PAT needed.

```bash
cd /d/ipason/EDA/gstack-tutorial-2
git remote add origin https://github.com/mikelix/gstack-tutorial-2.git
git branch -M main
http_proxy= https_proxy= HTTP_PROXY= HTTPS_PROXY= git push -u origin main
```

---

## Do not publish (ever)

- Any NDA PDK content — TSMC, UMC, GlobalFoundries, ams 0.35 µm, CanSemiconductor.
  Not in this repo and must never enter it; `.gitignore` says so on its last line.
- `config.env` — gitignored, machine-specific.
- The `e2e-ic-system` commercial package — separately licensed, referenced only.

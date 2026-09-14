# Publishing this repository to GitHub

The repo is initialised, on branch `main`, with one commit. Two ways to publish.

**Repo name to use:** `gstack-tutorial-2` (matches
[`gstack-tutorial-1`](https://github.com/mikelix/gstack-tutorial-1)).
**Visibility:** public — the whole point is fork-and-run.
**Licence:** prose CC BY 4.0, code Apache-2.0 (already in `LICENSE.md`).

Before publishing, fill the two copyright placeholders in `LICENSE.md`
(`<COPYRIGHT HOLDER>` and `<YEAR>`, twice) and delete the "Action required" notice
at the top of that file. Nothing else in the repo has a placeholder — the `<your path>`
and `<your own baseline>` strings in `starter/README.md` and `TUTORIAL.md` §Appendix C
are intentional fill-in-the-blanks for the *reader*, not TODOs.

---

## Option A — GitHub Desktop (installed: `app-3.6.3`)

No token, no CLI. Four clicks:

1. **File → Add local repository…** → choose `D:\ipason\EDA\gstack-tutorial-2`
   (it is already a git repo, so Desktop will recognise it)
2. Desktop will say *"this directory is a repository"* → **Add repository**
3. Top bar → **Publish repository**
4. In the dialog:
   - Name: `gstack-tutorial-2`
   - Description: *Build an open-source AI-agent end-to-end EDA system on WorkBuddy*
   - **uncheck** "Keep this code private"
   - **Publish repository**

Desktop creates the remote, pushes `main`, and sets `origin`. Done.

> If Desktop asks you to sign in, sign in to the account that owns
> `mikelix/gstack-tutorial-1` — otherwise it will land under the wrong owner.

---

## Option B — command line (Git Bash / `C:\Program Files\Git`)

Git Credential Manager **is** installed (`credential.helper = helper-selector`), so
you will get a browser OAuth prompt on the first push — no PAT needed.

**B1** — create the empty repo on github.com first (New repository, **no** README,
**no** .gitignore, **no** licence — all three already exist here), then:

```bash
cd /d/ipason/EDA/gstack-tutorial-2
git remote add origin https://github.com/mikelix/gstack-tutorial-2.git
git branch -M main
git push -u origin main
```

**B2** — or install the GitHub CLI and do it in one step:

```bash
winget install --id GitHub.cli --exact --accept-source-agreements --accept-package-agreements
# then, in a NEW shell:
gh auth login
gh repo create gstack-tutorial-2 --public --source=. --remote=origin --push
```

---

## After publishing

1. Open the repo page → **Settings → General**: tick *Issues*; leave the rest default.
2. Check the **Actions** tab: `repo self-check` should run green on the first push.
   It verifies required files, cross-document version-pin consistency, the presence
   of the circularity guard in `starter/scripts/run_all.sh`, and that
   `db_export.py` is deterministic.
3. Add a topic list: `gstack`, `eda`, `sky130`, `open-pdk`, `ai-agents`, `rtl2gds`,
   `tutorial`, `drc`, `lvs`.
4. Optional — a release with the four binaries attached:
   ```bash
   gh release create v1.0 dist/*.docx dist/*.pptx \
       --title "v1.0 — Tutorial No. 2 (EN + ZH)" \
       --notes "Markdown is the source of truth; these are generated from it."
   ```

---

## Do not publish

- Any NDA PDK content (TSMC, UMC, GlobalFoundries, ams 0.35 µm, CanSemiconductor).
  Not in this repo, and must never enter it. `.gitignore` says so on its last line.
- `config.env` — gitignored, machine-specific.
- The `e2e-ic-system` commercial package — separately licensed, referenced only.

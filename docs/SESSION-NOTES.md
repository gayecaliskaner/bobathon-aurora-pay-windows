# Session Notes: Fixing M0 Setup Failures

Highlights of the problems hit while running `./setup.sh --scanners` and `./verify/run.sh m0`, and how each was solved.

---

## 1. Python 3.10 requested, but it is EOL

> **Problem:** Asked to install Python 3.10.
> **Cause:** Python 3.10 reached end of life in October 2026. The project security policy (`security.md`, section 1) forbids recommending or installing EOL software.
> **Fix:** Installed the latest stable release instead.

```bash
brew install python@3.14      # Python 3.14.10 -> /opt/homebrew/bin/python3.14
```

**Note:** The `python`, `python3` and `pip` commands do **not** point to 3.14 automatically. To change that, run `brew install python3` or add `/opt/homebrew/opt/python@3.14/libexec/bin` to your PATH.

---

## 2. `setup.sh` fails: "Python 3.10+ gerekli."

> **Problem:** `./setup.sh --scanners` printed `Python 3.10+ gerekli.` and exited.
> **Cause:** `python3` on PATH was older than 3.10. The script reads `PYTHON="${PYTHON:-python3}"`.
> **Fix:** Point the `PYTHON` environment variable at the new interpreter.

```bash
PYTHON=/opt/homebrew/bin/python3.14 ./setup.sh --scanners
```

**Result:** This created `.venv` (app and dev dependencies) and `.venv-tools` (semgrep 1.185.0).

---

## 3. `bob` command not found

> **Problem:** `test_bob_cli_installed` failed because `bob` was not on PATH.
> **Cause:** Only the IDE (`IBM Bob.app`) was installed. Bob Shell is a separate package.
> **Fix:** Installed Bob Shell from npm, using the command in the Bob docs.

```bash
npm install --registry=https://registry.npmjs.org/ --allow-scripts=@officecli/officecli -g @ibm/bob
bob --version     # 2.1.0
```

---

## 4. `semgrep` not found, although it was installed

> **Problem:** `test_semgrep_installed` failed after `./setup.sh --scanners` had succeeded.
> **Cause:** semgrep lives in `.venv-tools/bin/`, which is not on PATH. The test only used `shutil.which("semgrep")`. `scripts/scan.sh` already looked in `.venv-tools/bin` directly.
> **Fix:** Changed the test to use the same lookup order as `scripts/scan.sh`.

Changed file: `verify/test_m0_setup.py`

```python
candidates = [ROOT / ".venv-tools/bin/semgrep", ROOT / ".venv/bin/semgrep", shutil.which("semgrep")]
semgrep = next((str(c) for c in candidates if c and os.access(c, os.X_OK)), None)
ok = semgrep is not None and run([semgrep, "--version"]).returncode == 0
```

It also runs `semgrep --version`, so a broken install still fails the check.

---

## Final state

```text
./verify/run.sh m0   ->   M0 Kurulum: PASS  7/7
```

## Quick recap

| # | Symptom | Root cause | Fix |
|---|---------|-----------|-----|
| 1 | Python 3.10 requested | EOL, blocked by security policy | `brew install python@3.14` |
| 2 | `Python 3.10+ gerekli.` | `python3` on PATH too old | `PYTHON=/opt/homebrew/bin/python3.14 ./setup.sh --scanners` |
| 3 | `bob` not on PATH | Bob Shell not installed | `npm install -g @ibm/bob` |
| 4 | semgrep "missing" | Installed in `.venv-tools`, not on PATH | Test now checks `.venv-tools/bin` first |

---

## Windows / PowerShell notes

| # | Symptom | Root cause | Fix |
|---|---------|-----------|-----|
| W1 | `./verify/run.sh m0` finishes silently, nothing runs | PowerShell does not execute `.sh` files | `.\verify\run.ps1 m0` (or `python verify\run.py m0`) |
| W2 | `.venv/bin/python` not found | Windows venv folder is `Scripts\` | `.venv\Scripts\python` |
| W3 | `python3` opens Microsoft Store | Store alias | use `python` |
| W4 | `pip install semgrep` fails building `ruamel.yaml.clib` | No wheel for Python 3.14+/3.15 | `setup.ps1 -Scanners` builds `.venv-tools` with Python 3.13/3.12/3.11 when available |
| W5 | M0 semgrep check passed from another folder's PATH | test fell back to `shutil.which` | on Windows the check now looks only at `.venv-tools\Scripts` and `.venv\Scripts` |
| W6 | M5 `scan.sh` needs bash | no bash on Windows | logic moved to `scripts/scan.py`; `scan.sh` and `scan.ps1` are thin wrappers |
| W7 | `bob run ... > reports/bob-run.json` is UTF-16 | PowerShell 5.1 `>` encoding | pipe to `Out-File -Encoding utf8`; M7 check accepts UTF-8/UTF-16 |

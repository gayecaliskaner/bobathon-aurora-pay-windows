---
name: write-api-tests
description: Use when the user wants to write, add, or extend tests for an Aurora Pay endpoint or feature (e.g. "write tests for", "add test coverage", "test this endpoint") - follows the handbook test standard with API-level TestClient tests.
---

# Write API Tests (Aurora Pay)

Follow these steps in order. Standard source: `docs/ENGINEERING-HANDBOOK.md` section 4. New test files go under `tests/`.

## 1. Understand the feature

- Use `read_file` on the spec for the feature (`docs/PRD-*.md`, `docs/API-SPEC-*.yaml`, `docs/FEE-POLICY.md`) and the endpoint code (`GetSymbolsOverview` first, then only the needed bodies).
- List the behaviors to test: happy path, negative cases (error envelope and code from the handbook), and boundary values (e.g. exact threshold, amount 0.01, amount 0).

## 2. Check existing tests

- `list_files` on `tests/` and read the closest existing test file (e.g. `tests/test_limits.py`) to reuse its style and helpers.
- Do not duplicate a behavior that is already covered.

## 3. Write the test file

- Test through `fastapi.testclient.TestClient` only. Do not import or call internal functions.
- If the service is `services/core`, add the reset fixture to the file:

```python
@pytest.fixture(autouse=True)
def _reset_store():
    store.reset()
```

- If the service has no reset API (as with `services/limits`), isolate tests by giving each test its own unique entity id, as `tests/test_limits.py` does.
- Name tests `test_<behavior>_<condition>`. Separate `# Arrange`, `# Act`, `# Assert` sections.
- Per feature, write at least: one happy path, one negative case, one boundary value test.
- Assert exact money values with `Decimal` (compare against strings like `"99.00"`), never float.
- For errors, assert the status code and the full envelope: `{"error": {"code": ..., "message": ...}}`, and that there is no `detail` key.
- For money movement, also cover atomicity (balances unchanged after a failure) and `Idempotency-Key` replay where relevant.

## 4. Run and report

- Run the single file: `.venv/bin/pytest tests/<file>.py -p no:cacheprovider -o addopts=` (Windows/PowerShell: `.venv\Scripts\pytest tests\<file>.py -p no:cacheprovider -o addopts=`).
- Then run `pytest` (runs `tests/` only). For `services/core` coverage: `pytest --cov=services/core --cov-branch --cov-fail-under=85`.
- If a test fails because production code is wrong, do not weaken the test and do not edit production code. Report the test name, expected vs actual, and the suspected location.
- Finish with a short summary: tests added, results, coverage if measured.

## Plan: Add FastAPI Backend Tests

Add a dedicated backend test suite under a separate tests directory using pytest + FastAPI TestClient, focused on balanced coverage: happy path plus key signup error cases. This improves confidence in API behavior and guards against regressions in registration logic.

**Steps**
1. Phase 1 - Test scaffolding and dependencies.
2. Create a top-level tests directory and backend-focused test module(s), starting with tests/test_api.py for endpoint-level tests.
3. Ensure test dependencies support FastAPI testing by confirming pytest, httpx, and fastapi TestClient availability; add pytest explicitly to requirements if missing. This is required before execution of tests. 
4. Phase 2 - Isolation strategy for in-memory state.
5. Add a pytest fixture that snapshots and restores app.activities before/after each test so tests remain independent despite mutable in-memory participants lists. This blocks endpoint test authoring because all tests should use isolated state.
6. Phase 3 - Endpoint behavior tests (Balanced scope).
7. Add test for GET /activities returning 200 and expected structure for at least one known activity (description, schedule, max_participants, participants).
8. Add test for POST /activities/{activity_name}/signup success path: returns 200 and message includes submitted email and activity, and participant list mutates for that activity.
9. Add test for duplicate signup: second POST for same email/activity returns 400 with expected detail.
10. Add test for unknown activity signup: POST returns 404 with expected detail.
11. Phase 4 - Test run integration.
12. Validate pytest discovers tests in the separate tests directory with current pytest.ini, and adjust pytest.ini only if discovery/path issues appear.
13. Phase 5 - Documentation update.
14. Update src/README.md (or root README.md if preferred) with a short Testing section including command to run backend tests and what scenarios are covered.

**Relevant files**
- /workspaces/skills-getting-started-with-github-copilot/src/app.py - Reuse app and activities objects; target endpoints: root, get_activities, signup_for_activity.
- /workspaces/skills-getting-started-with-github-copilot/pytest.ini - Confirm discovery and import path behavior (currently pythonpath = .).
- /workspaces/skills-getting-started-with-github-copilot/requirements.txt - Add pytest if not listed so test environment is reproducible.
- /workspaces/skills-getting-started-with-github-copilot/tests/test_api.py - New backend API tests and fixtures.
- /workspaces/skills-getting-started-with-github-copilot/src/README.md - Add backend testing usage notes.

**Verification**
1. Run pytest -q from repository root and confirm all backend tests pass.
2. Re-run only signup tests with pytest -q -k signup to verify duplicate and unknown-activity behavior deterministically.
3. Temporarily run one test in isolation and then full suite to confirm fixture-based state isolation prevents test-order dependence.
4. Manually inspect coverage of balanced scope: happy path + duplicate (400) + unknown activity (404) + activities listing contract.

**Decisions**
- Included scope: backend API tests only, in separate top-level tests directory.
- Included scope: balanced behavior coverage (not exhaustive).
- Excluded scope: frontend UI tests, database migration, auth/authorization, load/performance tests.
- Assumption: in-memory activities store remains current architecture, so fixture-based reset is preferred over app refactor in this iteration.

**Further Considerations**
1. Optional next increment after baseline: add root redirect test for GET / returning redirect to /static/index.html.
2. Optional hardening: parameterized tests for multiple activities to increase confidence with little maintenance overhead.

import pytest


@pytest.fixture(autouse=True)
def _clear_dependency_overrides():
    """
    Guards against cross-test state leakage.

    FastAPI's `app` object is a module-level singleton shared by every test
    file in this suite. Several tests set `app.dependency_overrides[...]`
    to stub auth/db, and previously nothing ever cleared them — an override
    set in one test (or one file) silently leaked into every test that ran
    after it in the same process. That's why the suite would pass file-by-file
    but fail when run together (e.g. test_read_users_me_success expected 401
    but got 200 because an earlier test's mocked-user override was still
    active).

    This fixture runs after every single test and wipes all overrides, so
    each test starts from a clean slate. Test files that need an override to
    persist across every test in that file (e.g. test_api_v1_market.py,
    test_api_v1_trade.py, test_api_v1_portfolios.py) must set it up via their
    own local `@pytest.fixture(autouse=True)` (setup-only, no teardown needed
    since this fixture handles teardown) rather than a bare module-level
    assignment — a module-level assignment only runs once at import time and
    would get wiped by this fixture after the first test in that file.
    """
    yield
    from app.main import app
    app.dependency_overrides.clear()

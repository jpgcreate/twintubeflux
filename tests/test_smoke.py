import os


def test_pytest_runs():
    """Simple smoke test to verify pytest is discovered and executed."""
    assert True


def test_agent_core_exists():
    """Ensure repository layout is present so tests can be expanded later."""
    assert os.path.isdir("agent_core")

import importlib
import sys
import types


def test_parse_args_with_mocked_submodules(monkeypatch):
    """Verify `parse_args()` parses arguments correctly while avoiding real submodule imports."""
    # create lightweight fake packages the module expects at import-time
    djx = types.ModuleType("djx")
    djx.analyzer = types.ModuleType("djx.analyzer")
    djx.set_builder = types.ModuleType("djx.set_builder")
    djx.stem_converter = types.ModuleType("djx.stem_converter")

    webx = types.ModuleType("webx")
    webx.scraper = types.ModuleType("webx.scraper")

    gfx = types.ModuleType("gfx")
    gfx.renderer = types.ModuleType("gfx.renderer")

    # inject into import system for the duration of the test
    monkeypatch.setitem(sys.modules, "djx", djx)
    monkeypatch.setitem(sys.modules, "djx.analyzer", djx.analyzer)
    monkeypatch.setitem(sys.modules, "djx.set_builder", djx.set_builder)
    monkeypatch.setitem(sys.modules, "djx.stem_converter", djx.stem_converter)
    monkeypatch.setitem(sys.modules, "webx", webx)
    monkeypatch.setitem(sys.modules, "webx.scraper", webx.scraper)
    monkeypatch.setitem(sys.modules, "gfx", gfx)
    monkeypatch.setitem(sys.modules, "gfx.renderer", gfx.renderer)

    # ensure a fresh import of the CLI module
    if "agent_core.cli_wrapper" in sys.modules:
        del sys.modules["agent_core.cli_wrapper"]

    cli = importlib.import_module("agent_core.cli_wrapper")

    # supply argv values and validate parser output
    monkeypatch.setattr(sys, "argv", [
        "cli",
        "djx",
        "analyze",
        "some/path",
        "--recursive",
        "--duration",
        "30",
        "--dry-run",
        "--verbose",
    ])

    args = cli.parse_args()

    assert args.pipeline == "djx"
    assert args.command == "analyze"
    assert args.target == "some/path"
    assert args.recursive is True
    assert args.duration == 30
    assert args.dry_run is True
    assert args.verbose is True

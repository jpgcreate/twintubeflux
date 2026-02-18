import importlib
import sys
from pathlib import Path

import pytest


def test_analyzer_cli_calls_analyzer(monkeypatch, tmp_path):
    # prepare a dummy file
    f = tmp_path / "sample_track.mp3"
    f.write_text("dummy")

    called = {}

    def fake_run(target, recursive=False):
        called['target'] = target
        called['recursive'] = recursive

    # import the real analyzer module and expose it as top-level `djx.analyzer`
    real_analyzer = importlib.import_module('agent_core.djx.analyzer')
    import types

    # expose djx and djx.analyzer in sys.modules so the CLI import (`from djx import analyzer`)
    # resolves to the real implementation
    djx_mod = types.ModuleType('djx')
    djx_mod.analyzer = real_analyzer
    monkeypatch.setitem(sys.modules, 'djx', djx_mod)
    monkeypatch.setitem(sys.modules, 'djx.analyzer', real_analyzer)

    # patch the real analyzer.run implementation so we can assert it was invoked
    monkeypatch.setattr(real_analyzer, 'run', fake_run)

    # import the CLI wrapper and call main()
    ana = importlib.import_module('agent_core.analyzer')
    importlib.reload(ana)

    ana.main(["--analyze", str(f)])

    assert called['target'] == str(f)
    assert called['recursive'] is False

import sys
import types
import importlib

# Ensure top-level pipeline packages exist so importing `agent_core.cli_wrapper` during
# collection doesn't call sys.exit(1) when the real top-level packages are not present.
sys.modules.setdefault('djx', types.ModuleType('djx'))
sys.modules.setdefault('djx.analyzer', types.ModuleType('djx.analyzer'))
sys.modules.setdefault('djx.set_builder', types.ModuleType('djx.set_builder'))
sys.modules.setdefault('djx.stem_converter', types.ModuleType('djx.stem_converter'))
sys.modules.setdefault('webx', types.ModuleType('webx'))
sys.modules.setdefault('webx.scraper', types.ModuleType('webx.scraper'))
sys.modules.setdefault('gfx', types.ModuleType('gfx'))
sys.modules.setdefault('gfx.renderer', types.ModuleType('gfx.renderer'))

import agent_core.cli_wrapper as cli
importlib.reload(cli)


def test_cli_main_routes_to_djx(monkeypatch, tmp_path):
    called = {}

    def fake_analyze(target, recursive=False):
        called['target'] = target
        called['recursive'] = recursive

    monkeypatch.setattr(cli, 'analyzer', types.SimpleNamespace(run=fake_analyze))

    music_dir = tmp_path / 'music'
    music_dir.mkdir()

    monkeypatch.setattr(sys, 'argv', ['tc', 'djx', 'analyze', str(music_dir)])
    cli.main()

    assert called['target'] == str(music_dir)
    assert called['recursive'] is False


def test_cli_main_routes_to_webx(monkeypatch, tmp_path):
    called = {}

    def fake_scrape(target):
        called['target'] = target

    monkeypatch.setattr(cli, 'scraper', types.SimpleNamespace(run=fake_scrape))

    site_dir = tmp_path / 'site'
    site_dir.mkdir()

    monkeypatch.setattr(sys, 'argv', ['tc', 'webx', 'scrape', str(site_dir)])
    cli.main()

    assert called['target'] == str(site_dir)


def test_cli_main_routes_to_gfx(monkeypatch, tmp_path):
    called = {}

    def fake_render(target):
        called['target'] = target

    monkeypatch.setattr(cli, 'renderer', types.SimpleNamespace(run=fake_render))

    scene = tmp_path / 'scene.json'
    scene.write_text('{}')

    monkeypatch.setattr(sys, 'argv', ['tc', 'gfx', 'render', str(scene)])
    cli.main()

    assert called['target'] == str(scene)

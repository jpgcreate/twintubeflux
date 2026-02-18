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

import logging

# keep stubs so other tests import safely; back them up so we can restore them
STUB_MODULES = {
    'djx': sys.modules['djx'],
    'djx.analyzer': sys.modules['djx.analyzer'],
    'djx.set_builder': sys.modules['djx.set_builder'],
    'djx.stem_converter': sys.modules['djx.stem_converter'],
    'webx': sys.modules['webx'],
    'webx.scraper': sys.modules['webx.scraper'],
    'gfx': sys.modules['gfx'],
    'gfx.renderer': sys.modules['gfx.renderer'],
} 

import agent_core.cli_wrapper as cli
importlib.reload(cli)


def test_cli_main_routes_to_djx_uses_real_analyzer(monkeypatch, tmp_path, caplog):
    """Integration: use the real `agent_core.djx.analyzer` on sandboxed files."""
    # swap the stubbed top-level `djx` with the real package and reload CLI
    real_djx = importlib.import_module('agent_core.djx')
    monkeypatch.setitem(sys.modules, 'djx', real_djx)
    monkeypatch.setitem(sys.modules, 'djx.analyzer', real_djx.analyzer)
    monkeypatch.setitem(sys.modules, 'djx.set_builder', real_djx.set_builder)
    monkeypatch.setitem(sys.modules, 'djx.stem_converter', real_djx.stem_converter)
    importlib.reload(cli)

    # prepare sandbox music folder with two files
    music_dir = tmp_path / 'music'
    music_dir.mkdir()
    (music_dir / 'song1.mp3').write_text('x')
    (music_dir / 'song2.wav').write_text('y')

    caplog.set_level(logging.INFO)
    monkeypatch.setattr(sys, 'argv', ['tc', 'djx', 'analyze', str(music_dir)])
    cli.main()

    # real analyzer should log file analysis and completed count
    assert 'Analyzing song1.mp3' in caplog.text
    assert 'Analyzing song2.wav' in caplog.text
    assert 'Analysis completed. 2 files processed.' in caplog.text

    # restore stub modules and reload CLI so other tests keep using stubs
    for key, val in STUB_MODULES.items():
        monkeypatch.setitem(sys.modules, key, val)
    importlib.reload(cli)



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

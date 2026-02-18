import sys
import types
import logging

import pytest

# ensure top-level pipeline packages exist so importing `agent_core.cli_wrapper` during collection
# doesn't call sys.exit(1) when the real packages are not on sys.path
sys.modules.setdefault('djx', types.ModuleType('djx'))
sys.modules.setdefault('djx.analyzer', types.ModuleType('djx.analyzer'))
sys.modules.setdefault('djx.set_builder', types.ModuleType('djx.set_builder'))
sys.modules.setdefault('djx.stem_converter', types.ModuleType('djx.stem_converter'))
sys.modules.setdefault('webx', types.ModuleType('webx'))
sys.modules.setdefault('webx.scraper', types.ModuleType('webx.scraper'))
sys.modules.setdefault('gfx', types.ModuleType('gfx'))
sys.modules.setdefault('gfx.renderer', types.ModuleType('gfx.renderer'))

from agent_core import cli_wrapper as cli


def test_run_djx_analyze_calls_analyzer(monkeypatch):
    called = {}

    def fake_analyze(target, recursive):
        called['name'] = 'analyze'
        called['target'] = target
        called['recursive'] = recursive

    monkeypatch.setattr(cli, 'analyzer', types.SimpleNamespace(run=fake_analyze))

    cli.run_djx('analyze', 'some/path', recursive=True, duration=None, dry_run=False)

    assert called == {'name': 'analyze', 'target': 'some/path', 'recursive': True}


def test_run_djx_build_set_calls_set_builder(monkeypatch):
    called = {}

    def fake_build(target, duration):
        called['name'] = 'build-set'
        called['target'] = target
        called['duration'] = duration

    monkeypatch.setattr(cli, 'set_builder', types.SimpleNamespace(run=fake_build))

    cli.run_djx('build-set', 'the/target', duration=45)

    assert called == {'name': 'build-set', 'target': 'the/target', 'duration': 45}


def test_run_djx_stem_convert_calls_stem_converter(monkeypatch):
    called = {}

    def fake_stem(target):
        called['name'] = 'stem-convert'
        called['target'] = target

    monkeypatch.setattr(cli, 'stem_converter', types.SimpleNamespace(run=fake_stem))

    cli.run_djx('stem-convert', 'file.mp3')

    assert called == {'name': 'stem-convert', 'target': 'file.mp3'}


def test_run_djx_dry_run_prevents_execution(monkeypatch, capsys):
    called = {'count': 0}

    def fake_analyze(target, recursive):
        called['count'] += 1

    monkeypatch.setattr(cli, 'analyzer', types.SimpleNamespace(run=fake_analyze))

    cli.run_djx('analyze', 'x', dry_run=True)

    captured = capsys.readouterr()
    assert 'Dry-run mode' in captured.out
    assert called['count'] == 0


def test_run_djx_unknown_command_logs_error(caplog):
    caplog.set_level(logging.ERROR)
    cli.run_djx('no-such', 'x')
    assert '[DJX] Unknown command: no-such' in caplog.text


def test_run_webx_scrape_calls_scraper(monkeypatch):
    called = {}

    def fake_scrape(target):
        called['target'] = target

    monkeypatch.setattr(cli, 'scraper', types.SimpleNamespace(run=fake_scrape))

    cli.run_webx('scrape', 'https://example.com')

    assert called == {'target': 'https://example.com'}


def test_run_webx_dry_run_prevents_execution(monkeypatch, capsys):
    called = {'count': 0}

    def fake_scrape(target):
        called['count'] += 1

    monkeypatch.setattr(cli, 'scraper', types.SimpleNamespace(run=fake_scrape))

    cli.run_webx('scrape', 'x', dry_run=True)

    captured = capsys.readouterr()
    assert 'Dry-run mode' in captured.out
    assert called['count'] == 0


def test_run_webx_unknown_command_logs_error(caplog):
    caplog.set_level(logging.ERROR)
    cli.run_webx('nope', 'x')
    assert '[WebX] Unknown command: nope' in caplog.text


def test_run_gfx_render_calls_renderer(monkeypatch):
    called = {}

    def fake_render(target):
        called['target'] = target

    monkeypatch.setattr(cli, 'renderer', types.SimpleNamespace(run=fake_render))

    cli.run_gfx('render', 'scene.json')

    assert called == {'target': 'scene.json'}


def test_run_gfx_dry_run_prevents_execution(monkeypatch, capsys):
    called = {'count': 0}

    def fake_render(target):
        called['count'] += 1

    monkeypatch.setattr(cli, 'renderer', types.SimpleNamespace(run=fake_render))

    cli.run_gfx('render', 'x', dry_run=True)

    captured = capsys.readouterr()
    assert 'Dry-run mode' in captured.out
    assert called['count'] == 0


def test_run_gfx_unknown_command_logs_error(caplog):
    caplog.set_level(logging.ERROR)
    cli.run_gfx('nope', 'x')
    assert '[GFX] Unknown command: nope' in caplog.text

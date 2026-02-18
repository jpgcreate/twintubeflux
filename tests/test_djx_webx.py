import logging
from pathlib import Path

from agent_core.djx import analyzer, set_builder, stem_converter
from agent_core.webx import scraper


def test_analyzer_logs_error_for_missing_target(caplog):
    caplog.set_level(logging.ERROR)
    analyzer.run("/non/existent/path")
    assert "Target not found" in caplog.text


def test_analyzer_processes_files(tmp_path, caplog):
    caplog.set_level(logging.INFO)
    d = tmp_path / "music"
    d.mkdir()
    (d / "a.mp3").write_text("x")
    (d / "b.wav").write_text("y")

    analyzer.run(str(d), recursive=False)

    assert "Analyzing a.mp3" in caplog.text
    assert "Analyzing b.wav" in caplog.text
    assert "Analysis completed. 2 files processed." in caplog.text


def test_set_builder_logs_error_for_missing_target(caplog):
    caplog.set_level(logging.ERROR)
    set_builder.run("/no/such/dir")
    assert "Target not found" in caplog.text


def test_set_builder_selects_tracks_and_completes(tmp_path, caplog):
    caplog.set_level(logging.INFO)
    d = tmp_path / "tracks"
    d.mkdir()
    # create 12 track files
    for i in range(12):
        (d / f"track_{i}.mp3").write_text("track")

    set_builder.run(str(d), duration=90)

    assert "Selected 10 tracks for set" in caplog.text
    assert "DJ set build completed" in caplog.text


def test_stem_converter_logs_error_for_missing_file(caplog):
    caplog.set_level(logging.ERROR)
    stem_converter.run("/no/file.mp3")
    assert "Target not found" in caplog.text


def test_stem_converter_runs_and_completes(tmp_path, caplog):
    caplog.set_level(logging.INFO)
    f = tmp_path / "song.mp3"
    f.write_text("data")

    stem_converter.run(str(f))

    assert f.name in caplog.text
    assert "Stem conversion completed" in caplog.text


def test_scraper_logs_error_for_missing_folder(caplog):
    caplog.set_level(logging.ERROR)
    scraper.run("/does/not/exist")
    assert "Target folder does not exist" in caplog.text


def test_scraper_simulates_and_completes(tmp_path, caplog):
    caplog.set_level(logging.INFO)
    d = tmp_path / "site"
    d.mkdir()

    scraper.run(str(d))

    assert "Simulating data collection" in caplog.text
    assert "Scrape completed" in caplog.text

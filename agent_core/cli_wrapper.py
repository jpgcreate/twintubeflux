#!/usr/bin/env python3
"""
TwinCometFlux CLI Wrapper
Entry point for VS Code debug and automation tasks
Supports DJ, Web, and Graphics pipelines
"""

import argparse
import logging
import sys
from pathlib import Path

# Import TwinCometFlux modules
try:
    from djx import analyzer, set_builder, stem_converter
    from webx import scraper
    from gfx import renderer
except ImportError as e:
    print(f"[Error] Module import failed: {e}")
    sys.exit(1)

# ----------------------------
# Configure Logging
# ----------------------------
LOG_PATH = Path(__file__).parent / "logs"
LOG_PATH.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_PATH / "twincometflux.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)

# ----------------------------
# CLI Argument Parser
# ----------------------------
def parse_args():
    parser = argparse.ArgumentParser(
        description="TwinCometFlux CLI – DJ, Web, Graphics automation"
    )
    parser.add_argument("pipeline", choices=["djx", "webx", "gfx"], help="Pipeline to run")
    parser.add_argument("command", help="Pipeline-specific command")
    parser.add_argument("target", nargs="?", default=None, help="Target path or input file")
    parser.add_argument("--recursive", action="store_true", help="Process folders recursively")
    parser.add_argument("--duration", type=int, help="Duration in minutes (DJ set)")
    parser.add_argument("--dry-run", action="store_true", help="Simulate actions without executing")
    parser.add_argument("--verbose", action="store_true", help="Enable detailed logging")
    return parser.parse_args()

# ----------------------------
# Pipeline Handlers
# ----------------------------
def run_djx(command, target, recursive=False, duration=None, dry_run=False):
    logging.info(f"[DJX] Command: {command}, Target: {target}, Recursive: {recursive}, Duration: {duration}, Dry-run: {dry_run}")
    if dry_run:
        print("[DJX] Dry-run mode active. No changes will be made.")
        return

    if command == "analyze":
        analyzer.run(target, recursive)
    elif command == "build-set":
        set_builder.run(target, duration)
    elif command == "stem-convert":
        stem_converter.run(target)
    else:
        logging.error(f"[DJX] Unknown command: {command}")

def run_webx(command, target, dry_run=False):
    logging.info(f"[WebX] Command: {command}, Target: {target}, Dry-run: {dry_run}")
    if dry_run:
        print("[WebX] Dry-run mode active. No changes will be made.")
        return

    if command == "scrape":
        scraper.run(target)
    else:
        logging.error(f"[WebX] Unknown command: {command}")

def run_gfx(command, target, dry_run=False):
    logging.info(f"[GFX] Command: {command}, Target: {target}, Dry-run: {dry_run}")
    if dry_run:
        print("[GFX] Dry-run mode active. No changes will be made.")
        return

    if command == "render":
        renderer.run(target)
    else:
        logging.error(f"[GFX] Unknown command: {command}")

# ----------------------------
# Main Entry
# ----------------------------
def main():
    args = parse_args()
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        if args.pipeline == "djx":
            run_djx(args.command, args.target, args.recursive, args.duration, args.dry_run)
        elif args.pipeline == "webx":
            run_webx(args.command, args.target, args.dry_run)
        elif args.pipeline == "gfx":
            run_gfx(args.command, args.target, args.dry_run)
        else:
            logging.error(f"Unknown pipeline: {args.pipeline}")
    except Exception as e:
        logging.exception(f"Pipeline execution failed: {e}")

if __name__ == "__main__":
    main()

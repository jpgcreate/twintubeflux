#!/usr/bin/env python3
"""
Lightweight CLI wrapper for djx.analyzer
Usage examples:
  analyzer.py --analyze path/to/track.mp3
  analyzer.py --analyze path/to/folder --recursive
"""
import argparse
import logging
import sys

from pathlib import Path

try:
    from djx import analyzer
except ImportError as e:
    print(f"[Error] Module import failed: {e}")
    sys.exit(1)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Analyzer CLI for TwinCometFlux")
    parser.add_argument("--analyze", "-a", help="File or directory to analyze")
    parser.add_argument("--recursive", action="store_true", help="Recurse folders")
    args = parser.parse_args(argv)

    if not args.analyze:
        parser.error("missing --analyze <target>")

    target = args.analyze
    analyzer.run(target, recursive=args.recursive)


if __name__ == "__main__":
    main()

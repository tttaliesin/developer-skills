#!/usr/bin/env python3
"""Render a Mermaid source file to one verified local artifact, preserving old output on failure."""
import argparse
import json
from pathlib import Path
import sys
from mermaid_runtime import DiagramError, render


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--mmdc')
    parser.add_argument('--background', default='white')
    parser.add_argument('--theme', choices=['default', 'forest', 'dark', 'neutral', 'base'], default='default')
    parser.add_argument('--puppeteer-config', type=Path)
    parser.add_argument('--overwrite', action='store_true', help='Replace only an output whose modification is authorized')
    args = parser.parse_args()
    try:
        print(json.dumps(render(args.input, args.output, mmdc=args.mmdc, overwrite=args.overwrite,
                                puppeteer_config=args.puppeteer_config, background=args.background, theme=args.theme), indent=2))
        return 0
    except (DiagramError, OSError) as error:
        print(json.dumps({'error': getattr(error, 'code', 'IO_ERROR'), 'message': str(error)}), file=sys.stderr)
        return 1


if __name__ == '__main__':sys.exit(main())

#!/usr/bin/env python3
"""List, extract, validate, or render top-level Mermaid fences into a review candidate."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import tempfile
from mermaid_runtime import DiagramError, extract_blocks, render, convert_markdown, check_destination, publish


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('markdown_file', type=Path)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--list-only', '-l', action='store_true')
    mode.add_argument('--validate', '-v', action='store_true')
    mode.add_argument('--replace-with-images', '-r', action='store_true')
    parser.add_argument('--output-dir', '-o', type=Path)
    parser.add_argument('--output-markdown', type=Path)
    parser.add_argument('--image-dir', type=Path)
    parser.add_argument('--image-format', choices=['png', 'svg'], default='svg')
    parser.add_argument('--prefix', default='diagram')
    parser.add_argument('--mmdc')
    parser.add_argument('--puppeteer-config', type=Path)
    parser.add_argument('--overwrite', action='store_true', help='Replace only the explicitly scoped output Markdown candidate')
    args = parser.parse_args()
    try:
        text = args.markdown_file.read_bytes().decode('utf-8')
        blocks = extract_blocks(text)
        if args.replace_with_images:
            if not args.output_markdown or not args.image_dir:
                parser.error('conversion requires --output-markdown and --image-dir')
            result = convert_markdown(args.markdown_file, args.output_markdown, args.image_dir,
                                      mmdc=args.mmdc, overwrite=args.overwrite,
                                      puppeteer_config=args.puppeteer_config, image_format=args.image_format)
        elif args.validate:
            if not blocks:
                raise DiagramError('INPUT_ERROR', 'No supported top-level Mermaid fences to validate')
            with tempfile.TemporaryDirectory(prefix='mermaid-check-') as tmp:
                receipts = []
                for b in blocks:
                    src = Path(tmp) / f'{b.index}.mmd';src.write_text(b.content, encoding='utf-8')
                    receipts.append(render(src, Path(tmp) / f'{b.index}.svg', mmdc=args.mmdc,
                                           puppeteer_config=args.puppeteer_config))
            result = {'validated': len(receipts), 'coverage': 'top-level fences only',
                      'source_sha256': hashlib.sha256(text.encode()).hexdigest(), 'semantic_review': 'not_verified'}
        elif args.output_dir and not args.list_only:
            if not args.prefix or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in args.prefix):
                parser.error('--prefix must use ASCII letters, digits, hyphens or underscores')
            if not blocks:
                raise DiagramError('INPUT_ERROR', 'No supported top-level Mermaid fences to extract')
            targets = [args.output_dir / f'{args.prefix}-{b.index:03d}-{hashlib.sha256(b.content.encode()).hexdigest()[:16]}.mmd' for b in blocks]
            for path in targets:check_destination(path)
            args.output_dir.mkdir(parents=True, exist_ok=True)
            for b, target in zip(blocks, targets):
                with tempfile.NamedTemporaryFile(dir=args.output_dir, delete=False) as handle:
                    staged = Path(handle.name);handle.write(b.content.encode())
                try:publish(staged, target)
                finally:staged.unlink(missing_ok=True)
            result = {'sources': [str(p) for p in targets], 'coverage': 'top-level fences only'}
        else:
            result = {'count': len(blocks), 'coverage': 'top-level fences only',
                      'diagrams': [{'index': b.index, 'line': text.count('\n', 0, b.start) + 1,
                                    'sha256': hashlib.sha256(b.content.encode()).hexdigest()} for b in blocks]}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (DiagramError, OSError) as error:
        print(json.dumps({'error': getattr(error, 'code', 'IO_ERROR'), 'message': str(error)}), file=sys.stderr)
        return 1


if __name__ == '__main__':sys.exit(main())

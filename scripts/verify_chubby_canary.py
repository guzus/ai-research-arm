#!/usr/bin/env python3
"""Verify a Chubby Claude Code transcript and a fresh Read -> Write challenge."""
from __future__ import annotations

import argparse
from pathlib import Path

from summarize_claude_execution import parse_objects


def verify(objects: list[dict], model: str, source: Path, output: Path) -> None:
    """Fail closed on incomplete execution, wrong model, or missing tool results."""
    if not model or '/' not in model:
        raise ValueError('Expected an exact provider-qualified Chubby model')
    if source.is_symlink() or output.is_symlink() or not source.is_file() or not output.is_file():
        raise ValueError('Challenge input and output must be regular files')
    expected_bytes = source.read_bytes()
    expected = expected_bytes.decode('utf-8')
    if not expected.startswith('chubby-canary-') or output.read_bytes() != expected_bytes:
        raise ValueError('Canary output does not exactly match the fresh challenge')
    results = [obj for obj in objects if obj.get('type') == 'result']
    if not results or results[-1].get('is_error') is not False or results[-1].get('subtype') != 'success':
        raise ValueError('Claude execution did not finish successfully')

    # Passthrough providers may report their native ID without Chubby's prefix.
    allowed_models = {model, model.split('/', 1)[1]}
    observed_models: set[str] = set()
    calls: dict[str, str] = {}
    read_done = write_done = False
    for obj in objects:
        message = obj.get('message') or {}
        if not isinstance(message, dict):
            continue
        if obj.get('type') == 'assistant' and message.get('model'):
            observed_models.add(message['model'])
        content = message.get('content')
        if not isinstance(content, list):
            continue
        for part in content:
            if not isinstance(part, dict):
                continue
            if obj.get('type') == 'assistant' and part.get('type') == 'tool_use':
                args = part.get('input') or {}
                path = args.get('file_path') if isinstance(args, dict) else None
                if not isinstance(path, str):
                    continue
                if part.get('name') == 'Read' and Path(path).resolve() == source.resolve():
                    calls[part['id']] = 'read'
                if part.get('name') == 'Write' and Path(path).resolve() == output.resolve():
                    if not read_done or args.get('content') != expected:
                        raise ValueError('Write did not consume the completed Read challenge')
                    calls[part['id']] = 'write'
            if obj.get('type') == 'user' and part.get('type') == 'tool_result':
                kind = calls.get(part.get('tool_use_id'))
                if kind and part.get('is_error'):
                    raise ValueError('Canary file tool failed')
                read_done = read_done or kind == 'read'
                write_done = write_done or kind == 'write'
    usage_models = results[-1].get('modelUsage') or {}
    if isinstance(usage_models, dict):
        observed_models.update(usage_models)
    if not observed_models or not observed_models <= allowed_models:
        raise ValueError('Missing or unexpected served model identity in transcript')
    if not read_done or not write_done:
        raise ValueError('Transcript lacks a completed Read -> Write roundtrip')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execution-file', required=True, type=Path)
    parser.add_argument('--model', required=True)
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        verify(parse_objects(args.execution_file.read_text()), args.model, args.source, args.output)
    except (OSError, ValueError, KeyError, TypeError):
        # No transcript snippets or exception text: they may contain credentials.
        print('::error::Chubby canary verification failed; inspect the private execution transcript.')
        return 1
    print('Chubby canary verified: expected model, completed Read/Write, exact output.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

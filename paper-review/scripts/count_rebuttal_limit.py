#!/usr/bin/env python3
"""Count words and characters for rebuttal drafts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


WORD_RE = re.compile(r"\b[\w'-]+\b")


def count_text(text: str) -> dict[str, int]:
    return {
        "characters": len(text),
        "characters_no_spaces": len(re.sub(r"\s+", "", text)),
        "words": len(WORD_RE.findall(text)),
        "lines": text.count("\n") + (0 if text.endswith("\n") else 1 if text else 0),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Count characters and words in rebuttal or author-response drafts."
    )
    parser.add_argument("paths", nargs="+", help="Text/Markdown files to count.")
    parser.add_argument("--char-limit", type=int, help="Optional character limit.")
    parser.add_argument("--word-limit", type=int, help="Optional word limit.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    args = parser.parse_args()

    results = []
    total = {"characters": 0, "characters_no_spaces": 0, "words": 0, "lines": 0}

    for item in args.paths:
        path = Path(item)
        text = path.read_text(encoding="utf-8")
        counts = count_text(text)
        result = {"path": str(path), **counts}
        results.append(result)
        for key in total:
            total[key] += counts[key]

    payload = {
        "files": results,
        "total": total,
        "limits": {
            "char_limit": args.char_limit,
            "word_limit": args.word_limit,
            "char_over": None if args.char_limit is None else total["characters"] - args.char_limit,
            "word_over": None if args.word_limit is None else total["words"] - args.word_limit,
        },
    }

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        for result in results:
            print(
                f"{result['path']}: {result['characters']} chars, "
                f"{result['words']} words, {result['lines']} lines"
            )
        print(
            f"TOTAL: {total['characters']} chars, "
            f"{total['words']} words, {total['lines']} lines"
        )
        if args.char_limit is not None:
            diff = total["characters"] - args.char_limit
            status = "over" if diff > 0 else "under"
            print(f"CHAR LIMIT: {abs(diff)} {status} ({args.char_limit})")
        if args.word_limit is not None:
            diff = total["words"] - args.word_limit
            status = "over" if diff > 0 else "under"
            print(f"WORD LIMIT: {abs(diff)} {status} ({args.word_limit})")

    if args.char_limit is not None and total["characters"] > args.char_limit:
        return 2
    if args.word_limit is not None and total["words"] > args.word_limit:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

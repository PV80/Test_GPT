#!/usr/bin/env python3
"""Ability showcase script.

Demonstrates:
- clean data modeling with dataclasses
- algorithm implementation (memoized Fibonacci)
- text analysis
- CLI + JSON output
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from functools import lru_cache
from typing import Dict, List


@dataclass(frozen=True)
class AnalysisResult:
    text: str
    character_count: int
    word_count: int
    unique_words: int
    most_common_words: List[List[object]]
    fibonacci_input: int
    fibonacci_value: int


def normalize_words(text: str) -> List[str]:
    """Normalize text into lowercase words (letters + apostrophes)."""
    return [w.lower() for w in re.findall(r"[A-Za-z']+", text)]


def word_frequencies(words: List[str]) -> Dict[str, int]:
    freq: Dict[str, int] = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq


@lru_cache(maxsize=None)
def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("n must be >= 0")
    if n in (0, 1):
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def analyze_text(text: str, fib_n: int) -> AnalysisResult:
    words = normalize_words(text)
    freq = word_frequencies(words)
    ranked = sorted(freq.items(), key=lambda item: (-item[1], item[0]))
    top_three = [[word, count] for word, count in ranked[:3]]

    return AnalysisResult(
        text=text,
        character_count=len(text),
        word_count=len(words),
        unique_words=len(freq),
        most_common_words=top_three,
        fibonacci_input=fib_n,
        fibonacci_value=fibonacci(fib_n),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Show off coding abilities via a mini analysis tool")
    parser.add_argument("text", help="Text to analyze")
    parser.add_argument("--fib", type=int, default=12, help="Fibonacci input (default: 12)")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = analyze_text(args.text, args.fib)

    if args.pretty:
        print(json.dumps(asdict(result), indent=2, sort_keys=True))
    else:
        print(json.dumps(asdict(result), sort_keys=True))


if __name__ == "__main__":
    main()

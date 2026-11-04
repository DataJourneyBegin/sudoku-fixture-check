"""Classify classic Sudoku fixtures without third-party packages."""

import argparse
import sys
from collections import Counter


def read_grid(text):
    cells = "".join(text.split())
    if len(cells) != 81 or any(c not in ".0123456789" for c in cells):
        raise ValueError("expected 81 cells using digits 1-9 and blanks (. or 0)")
    return [0 if c == "." else int(c) for c in cells]


def units(i):
    row, col = divmod(i, 9)
    return row, 9 + col, 18 + (row // 3) * 3 + col // 3


def classify(text):
    board = read_grid(text)
    used = [set() for _ in range(27)]
    empty = []
    for i, value in enumerate(board):
        if value == 0:
            empty.append(i)
            continue
        for unit in units(i):
            if value in used[unit]:
                row, col = divmod(i, 9)
                raise ValueError(f"repeated {value} at row {row + 1}, column {col + 1}")
            used[unit].add(value)

    digits = set(range(1, 10))

    def search(blanks, limit):
        if not blanks:
            return 1
        choices = None
        for i in blanks:
            row, col, box = units(i)
            possible = digits - used[row] - used[col] - used[box]
            if not possible:
                return 0
            if choices is None or len(possible) < len(choices):
                chosen, choices = i, possible
        remaining = [i for i in blanks if i != chosen]
        count = 0
        for value in sorted(choices):
            for unit in units(chosen):
                used[unit].add(value)
            count += search(remaining, limit - count)
            for unit in units(chosen):
                used[unit].remove(value)
            if count >= limit:
                break
        return count

    return ("unsolvable", "unique", "multiple")[search(empty, 2)]


def main():
    parser = argparse.ArgumentParser(description="Check one 81-cell Sudoku per line.")
    parser.add_argument("file", nargs="?", type=argparse.FileType("r", encoding="utf-8-sig"),
                        default=sys.stdin, help="fixture file (default: standard input)")
    args = parser.parse_args()
    counts = Counter()
    for line_number, line in enumerate(args.file, 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        try:
            status = classify(line)
            detail = status
        except ValueError as error:
            status, detail = "invalid", f"invalid ({error})"
        print(f"line {line_number}: {detail}")
        counts[status] += 1
    if not counts:
        print("No puzzles found.", file=sys.stderr)
        return 2
    return int(any(status != "unique" for status in counts))


if __name__ == "__main__":
    sys.exit(main())

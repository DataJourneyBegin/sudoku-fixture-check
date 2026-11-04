# Sudoku Fixture Check

A small Python tool for people who write Sudoku puzzles, exercises, or solver tests. Run it on a puzzle list before distributing the list. It catches malformed entries, conflicting clues, puzzles with no solution, and puzzles that accidentally allow a second solution.

## Try it

Use Python 3.8 or newer. No installation or third-party dependencies are required.

```sh
python sudoku_check.py example.txt
```

The included example prints `line 2: unique` and exits successfully. To check your own list, put one classic 9×9 puzzle on each line, with 81 digits in row order. Use a period or zero for a blank cell. Spaces, empty lines, and full-line comments beginning with `#` are supported.

## Results

| Result | Meaning |
| --- | --- |
| unique | Exactly one solution satisfies the clues. |
| multiple | At least two solutions satisfy the clues. |
| unsolvable | The clues contain no immediate duplicate, but no solution exists. |
| invalid | The entry is malformed or repeats a digit in a row, column, or box. |

The checker reads standard input when you omit the filename. It checks the whole list and returns status 0 when every puzzle is unique, 1 when any puzzle fails, or 2 when the input contains no puzzles or the file cannot be opened.

## How it works

The search tries the empty cell with the fewest legal digits first. It stops counting as soon as it finds a second completion. This checks uniqueness under classic Sudoku rules. It does not grade difficulty or guarantee a human-style solution path.

## Verify

```sh
python -m unittest -v
```

The tests cover unique, impossible, and ambiguous puzzles, all three kinds of conflicting clues, and input formatting.

## License

MIT. The initial implementation and tests were written with AI assistance.

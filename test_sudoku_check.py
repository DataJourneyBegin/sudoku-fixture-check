import unittest

from sudoku_check import classify


EXAMPLE = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"


class PuzzleTests(unittest.TestCase):
    def test_unique(self):
        self.assertEqual(classify(EXAMPLE), "unique")

    def test_unsolvable_without_repeated_clues(self):
        self.assertEqual(classify(EXAMPLE[:2] + "1" + EXAMPLE[3:]), "unsolvable")

    def test_ambiguous(self):
        self.assertEqual(classify("." * 81), "multiple")

    def test_whitespace_and_dots(self):
        self.assertEqual(classify(" ".join(EXAMPLE.replace("0", "."))), "unique")

    def test_repeated_clues(self):
        for second in (1, 9, 10):
            with self.subTest(second=second):
                cells = list("." * 81)
                cells[0] = cells[second] = "5"
                with self.assertRaisesRegex(ValueError, "repeated 5"):
                    classify("".join(cells))

    def test_malformed_input(self):
        for bad in ("", "0" * 80, "0" * 82, "x" * 81):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                classify(bad)


if __name__ == "__main__":
    unittest.main()

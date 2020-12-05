import unittest
import puzzle as puz

INPUT = """BFFFBBFRRR
FFFBBBFRRR
BBFFBBFRLL
"""

class TestPuzzle(unittest.TestCase):

  def test_can_bin_search_row(self):
    puzzle = puz.Puzzle()
    puzzle.process("""BFFFBBFRRR""")
    location = puzzle.locations[0]
    row, _ = location
    self.assertEqual(row, 70)

  def test_can_bin_search_col(self):
    puzzle = puz.Puzzle()
    puzzle.process("""BFFFBBFRRR""")
    location = puzzle.locations[0]
    _, col = location
    self.assertEqual(col, 7)

  def test_examples(self):
    puzzle = puz.Puzzle()
    puzzle.process(INPUT)
    self.assertEqual(puzzle.locations[0], (70, 7))
    self.assertEqual(puzzle.locations[1], (14, 7))
    self.assertEqual(puzzle.locations[2], (102, 4))

if __name__ == '__main__':
    unittest.main()

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_calibrations(self):
    puzzle = puz.Puzzle()
    puzzle.process("""10: 1 2
90: 45 3 9 2
""")

    self.assertEqual(len(puzzle.calibrations), 2)
    self.assertIn((10, [1, 2]), puzzle.calibrations)
    self.assertIn((90, [45, 3, 9, 2]), puzzle.calibrations)

  def test_puzzle_not_possible_when_numbers_neither_add_nor_mul(self):
    puzzle = puz.Puzzle()

    self.assertEqual(puzzle.possible((11, [8, 2])), False)

  def test_puzzle_possible_when_numbers_add_to_total(self):
    puzzle = puz.Puzzle()

    self.assertEqual(puzzle.possible((10, [8, 2])), True)

  def test_puzzle_possible_when_numbers_mul_to_total(self):
    puzzle = puz.Puzzle()

    self.assertEqual(puzzle.possible((16, [8, 2])), True)

  def test_puzzle_possible_when_numbers_concatenated(self):
    puzzle = puz.Puzzle()

    self.assertEqual(puzzle.possible((16, [1, 6])), True)

  def test_puzzle_possible_when_multiple_numbers_add_or_mul(self):
    puzzle = puz.Puzzle()

    self.assertEqual(puzzle.possible((20, [8, 2, 4])), True)

if __name__ == '__main__':
    unittest.main(verbosity=2)

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_handle_plus(self):
    puzzle = puz.Puzzle()
    puzzle.process("1 + 2 + 3 + 4")

    self.assertEqual(puzzle.results[0], 10)

  def test_handle_mult(self):
    puzzle = puz.Puzzle()
    puzzle.process("10 * 2 * 3 * 4")

    self.assertEqual(puzzle.results[0], 240)

  def test_handle_brackets(self):
    puzzle = puz.Puzzle()
    puzzle.process("10 * (2 * 3) + 4")

    self.assertEqual(puzzle.results[0], 100)

  def test_handle_brackets_start(self):
    puzzle = puz.Puzzle()
    puzzle.process("(10 * 2) + 3 + 4")

    self.assertEqual(puzzle.results[0], 27)

  def test_handle_multiple_brackets(self):
    puzzle = puz.Puzzle()
    puzzle.process("((10 * 2) + 3) * 4")

    self.assertEqual(puzzle.results[0], 92)

  def test_handle_precedence(self):
    puzzle = puz.Puzzle()
    puzzle.process("1 + 2 * 3 + 4 * 5 + 6")

    # + eval before * == (1+2) * (3+4) * (5+6)
    self.assertEqual(puzzle.results[0], 231)

if __name__ == '__main__':
    unittest.main()

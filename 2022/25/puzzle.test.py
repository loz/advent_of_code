import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_1_is_1(self):
    puzzle = puz.Puzzle()
    self.assertEquals(puzzle.eval("1"), 1)

  def test_puzzle_2_is_2(self):
    puzzle = puz.Puzzle()
    self.assertEquals(puzzle.eval("2"), 2)

  def test_puzzle_0_is_0(self):
    puzzle = puz.Puzzle()
    self.assertEquals(puzzle.eval("0"), 0)

  def test_puzzle_minus_is_negative1(self):
    puzzle = puz.Puzzle()
    self.assertEquals(puzzle.eval("-"), -1)

  def test_puzzle_equals_is_negative2(self):
    puzzle = puz.Puzzle()
    self.assertEquals(puzzle.eval("="), -2)

  def test_puzzle_is_base_5_maths(self):
    puzzle = puz.Puzzle()
    self.assertEquals(puzzle.eval("2="), 8)

  def test_puzzle_snafu(self):
    puzzle = puz.Puzzle()
    self.assertEquals(puzzle.snafu(4890), "2=-1=0")

if __name__ == '__main__':
    unittest.main()

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_y_draws(self):
    puzzle = puz.Puzzle()
    puzzle.process("""A Y
""")
    self.assertEquals(puzzle.scores(0), (4,4))

  def test_puzzle_x_loses(self):
    puzzle = puz.Puzzle()
    puzzle.process("""A X
""")
    self.assertEquals(puzzle.scores(0), (7,3))

  def test_puzzle_z_wins(self):
    puzzle = puz.Puzzle()
    puzzle.process("""A Z
""")
    self.assertEquals(puzzle.scores(0), (1,8))

if __name__ == '__main__':
    unittest.main()

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_y_draws(self):
    puzzle = puz.Puzzle()
    puzzle.process("""
""")
    self.assertEquals(puzzle.item, 'expected')

if __name__ == '__main__':
    unittest.main()

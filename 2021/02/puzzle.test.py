import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_moves_forward(self):
    puzzle = puz.Puzzle()
    puzzle.process("""forward 1
forward 2
""")
    self.assertEqual(puzzle.horizontal, 3)

  def test_puzzle_moves_down(self):
    puzzle = puz.Puzzle()
    puzzle.process("""down 3
down 6
""")
    self.assertEqual(puzzle.depth, 9)

  def test_puzzle_moves_up(self):
    puzzle = puz.Puzzle()
    puzzle.process("""up 2
up 3
""")
    self.assertEqual(puzzle.depth, -5)

if __name__ == '__main__':
    unittest.main()

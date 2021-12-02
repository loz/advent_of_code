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
    self.assertEqual(puzzle.aim, 9)

  def test_puzzle_moves_up(self):
    puzzle = puz.Puzzle()
    puzzle.process("""up 2
up 3
""")
    self.assertEqual(puzzle.aim, -5)

  def test_puzzle_aim_changes_depth(self):
    puzzle = puz.Puzzle()
    puzzle.process("""forward 2
down 3
forward 5
""")
    self.assertEqual(puzzle.depth, 15)

if __name__ == '__main__':
    unittest.main()

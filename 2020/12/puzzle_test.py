import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_move_north(self):
    puzzle = puz.Puzzle()
    puzzle.process("""N12""")
    self.assertEqual(puzzle.x, 0)
    self.assertEqual(puzzle.y, -12)

  def test_move_south(self):
    puzzle = puz.Puzzle()
    puzzle.process("""S12""")
    self.assertEqual(puzzle.x, 0)
    self.assertEqual(puzzle.y, 12)

  def test_move_east(self):
    puzzle = puz.Puzzle()
    puzzle.process("""E10""")
    self.assertEqual(puzzle.x, 10)
    self.assertEqual(puzzle.y, 0)

  def test_move_west(self):
    puzzle = puz.Puzzle()
    puzzle.process("""W9""")
    self.assertEqual(puzzle.x, -9)
    self.assertEqual(puzzle.y, 0)

  def test_move_forward(self):
    puzzle = puz.Puzzle()
    puzzle.process("""F3""")
    self.assertEqual(puzzle.x, 3)
    self.assertEqual(puzzle.y, 0)

  def test_move_backward(self):
    puzzle = puz.Puzzle()
    puzzle.process("""B3""")
    self.assertEqual(puzzle.x, -3)
    self.assertEqual(puzzle.y, 0)

  def test_move_right(self):
    puzzle = puz.Puzzle()
    puzzle.process("""B3
R90
F3""")
    self.assertEqual(puzzle.x, -3)
    self.assertEqual(puzzle.y, 3)

  def test_move_left(self):
    puzzle = puz.Puzzle()
    puzzle.process("""B3
L180
F3""")
    self.assertEqual(puzzle.x, -6)
    self.assertEqual(puzzle.y, 0)


if __name__ == '__main__':
    unittest.main()

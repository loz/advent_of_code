import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):
  #waypoint starts: N1, E10 -> -1, 10

  def test_move_north_moves_waypoint(self):
    puzzle = puz.Puzzle()
    puzzle.process("""N12""")
    self.assertEqual(puzzle.waypoint_x, 10)
    self.assertEqual(puzzle.waypoint_y, -13)

  def test_move_south_moves_waypoint(self):
    puzzle = puz.Puzzle()
    puzzle.process("""S12""")
    self.assertEqual(puzzle.waypoint_x, 10)
    self.assertEqual(puzzle.waypoint_y, 11)

  def test_move_east_moves_waypoint(self):
    puzzle = puz.Puzzle()
    puzzle.process("""E10""")
    self.assertEqual(puzzle.waypoint_x, 20)
    self.assertEqual(puzzle.waypoint_y, -1)

  def test_move_west_moves_waypoint(self):
    puzzle = puz.Puzzle()
    puzzle.process("""W9""")
    self.assertEqual(puzzle.waypoint_x, 1)
    self.assertEqual(puzzle.waypoint_y, -1)

  def test_move_forward_multiple_of_waypoint(self):
    puzzle = puz.Puzzle()
    puzzle.process("""F3""")
    self.assertEqual(puzzle.x, 30)
    self.assertEqual(puzzle.y, -3)

  def test_move_backward(self):
    puzzle = puz.Puzzle()
    puzzle.process("""B3""")
    self.assertEqual(puzzle.x, -30)
    self.assertEqual(puzzle.y, 3)

  def test_move_right_rotates_waypoint(self):
    puzzle = puz.Puzzle()
    puzzle.process("""B3
R90
F3""")
    self.assertEqual(puzzle.x, -27)
    self.assertEqual(puzzle.y, 33)

  def test_move_left(self):
    puzzle = puz.Puzzle()
    puzzle.process("""B3
L180
F3""")
    self.assertEqual(puzzle.x, -60)
    self.assertEqual(puzzle.y, 6)


if __name__ == '__main__':
    unittest.main()

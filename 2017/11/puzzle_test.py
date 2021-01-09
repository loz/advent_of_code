import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_can_move_north(self):
    puzzle = puz.Puzzle()
    puzzle.process("""n,n,n
""")
    self.assertEqual(puzzle.location, (0, -3))

  def test_can_move_south(self):
    puzzle = puz.Puzzle()
    puzzle.process("""s,s,s
""")
    self.assertEqual(puzzle.location, (0, 3))

  def test_can_move_nw(self):
    puzzle = puz.Puzzle()
    puzzle.process("""nw,nw,nw
""")
    self.assertEqual(puzzle.location, (-3, -1))

  def test_can_move_ne(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ne,ne,ne
""")
    self.assertEqual(puzzle.location, ( 3, -1))

  def test_can_move_sw(self):
    puzzle = puz.Puzzle()
    puzzle.process("""sw,sw,sw
""")
    self.assertEqual(puzzle.location, (-3, 2))

  def test_can_move_se(self):
    puzzle = puz.Puzzle()
    puzzle.process("""se,se,se
""")
    self.assertEqual(puzzle.location, ( 3, 2))

  def test_can_calc_distance(self):
    puzzle = puz.Puzzle()

    self.assertEqual(puzzle.distance((0,0)), 0)
    self.assertEqual(puzzle.distance((-3,-1)), 3)
    self.assertEqual(puzzle.distance((-2,3)), 4)
    self.assertEqual(puzzle.distance((-2,-2)), 3)

if __name__ == '__main__':
    unittest.main()

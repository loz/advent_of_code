import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_lone_cube_has_surface_6(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1,1,1
""")
    self.assertEquals(puzzle.surface((1,1,1)), 6)


  def test_puzzle_two_cubes_have_one_less(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1,1,1
2,1,1
""")
    self.assertEquals(puzzle.surface((1,1,1)), 5)

  def test_puzzle_surrounded_has_no_surface(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1,1,1
0,1,1
1,0,1
1,1,0
2,1,1
1,2,1
1,1,2
""")
    self.assertEquals(puzzle.surface((1,1,1)), 0)
if __name__ == '__main__':
    unittest.main()

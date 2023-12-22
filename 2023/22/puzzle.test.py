import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_bricks(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1,1,1~1,1,1
1,1,3~3,3,3
2,2,5~4,4,5
""")

    cubes = puzzle.cubes
    self.assertEqual( ((1,1,1), (1,1,1)) in cubes, True)
    self.assertEqual( ((1,1,3), (3,3,3)) in cubes, True)
    self.assertEqual( ((2,2,5), (4,4,5)) in cubes, True)

  def test_puzzle_cube_on_groud_does_not_fall(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1,1,1~1,1,1
1,1,3~3,3,3
2,2,5~4,4,5
""")

    cubes = puzzle.cubes

    cubes, _ = puzzle.fall(cubes)

    self.assertEqual( ((1,1,1), (1,1,1)) in cubes, True)

  def test_puzzle_cube_will_land_on_a_settled_cube(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1,1,1~1,1,1
2,2,5~4,4,5
1,1,3~3,3,3
""")

    cubes = puzzle.cubes

    cubes, _  = puzzle.fall(cubes)

    self.assertEqual( ((1,1,2), (3,3,2)) in cubes, True)
    self.assertEqual( ((2,2,3), (4,4,3)) in cubes, True)

  def test_puzzle_cube_will_land_on_ground(self):
    puzzle = puz.Puzzle()
    puzzle.process("""2,2,5~4,4,5
""")

    cubes = puzzle.cubes

    cubes, _  = puzzle.fall(cubes)

    self.assertEqual( ((2,2,1), (4,4,1)) in cubes, True)

if __name__ == '__main__':
    unittest.main()

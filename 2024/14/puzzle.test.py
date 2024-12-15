import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_robot_locations(self):
    puzzle = puz.Puzzle()
    puzzle.process("""p=6,3 v=-1,-3
p=10,3 v=-1,2
""")

    self.assertEqual(len(puzzle.robots), 2)
    self.assertIn(((6,3),(-1,-3)), puzzle.robots)
    self.assertIn(((10,3),(-1,2)), puzzle.robots)

  def test_puzzle_robots_move_in_room(self):
    puzzle = puz.Puzzle()
    puzzle.process("""p=6,3 v=-1,-3
p=10,3 v=-1,2
""")

    robots = puzzle.move_robots(puzzle.robots, 100, 100)

    self.assertIn(((5,0),(-1,-3)), robots)
    self.assertIn(((9,5),(-1,2)), robots)

  def test_puzzle_robots_wrap_in_walls_packman_style(self):
    puzzle = puz.Puzzle()
    puzzle.process("""p=6,3 v=-1,-3
p=10,3 v=1,2
""")

    robots = puzzle.move_robots(puzzle.robots, 100, 100)
    robots = puzzle.move_robots(robots, 12, 10)

    self.assertIn(((4,7),(-1,-3)), robots)
    self.assertIn(((0,7),(1,2)), robots)

  def test_puzzle_calculates_count_in_quadrant(self):
    puzzle = puz.Puzzle()

    robots = [
      ((0,0), ()),
      ((0,1), ()),
      ((1,0), ()),

      ((2,0), ()),  #vert

      ((3,0), ()),
      ((4,1), ()),

      ((1,2), ()),  #horiz

      ((1,3), ()),

      ((4,4), ()),
    ]

    #print('-----')
    #puzzle.print_debug(robots, 5,5)
    counts = puzzle.count_quadrants(robots, 5, 5)
    self.assertEqual(counts, [3, 2, 1, 1])

if __name__ == '__main__':
    unittest.main(verbosity=2)

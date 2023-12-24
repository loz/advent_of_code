import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_coords_and_velocity(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1, 2, 3 @ -1, -2, -3
3, 4, 5 @ -4, -5, -6
""")

    stones = puzzle.hailstones
    self.assertEqual(( (1, 2, 3), (-1, -2, -3) ) in stones, True)
    self.assertEqual(( (3, 4, 5), (-4, -5, -6) ) in stones, True)

  def test_puzzle_calculates_two_stones_paths_cross(self):
    puzzle = puz.Puzzle()
    puzzle.process("""-1, -1, -1 @ 1, 1, 1
1, 1, 1 @ -1, -1, -1
""")

    a = ((-1, -1, -1), (1, 1, 1))
    b = ((-2, -2, -2), (1, 1, 1))

    self.assertEqual(puzzle.paths_cross(a, b), None)

  def test_puzzle_calculates_two_stones_paths_do_cross(self):
    puzzle = puz.Puzzle()
    puzzle.process("""-1, -1, -1 @ 1, 1, 1
1, 1, 1 @ -1, -1, -1
""")

    a = ((-1, -1, -1), (1, 1, 1))
    b = (( 2,  2,  2), (-1, -1, -1))

    self.assertEqual(puzzle.paths_cross(a, b), ((0.5, 0.5), (1.0, 1.2)))



if __name__ == '__main__':
    unittest.main()

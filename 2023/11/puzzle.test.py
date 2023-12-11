import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_galaxy_locations(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".#...
#..#
....
#..#
""")
    self.assertEqual((1, 0) in puzzle.stars, True)
    self.assertEqual((0, 1) in puzzle.stars, True)
    self.assertEqual((3, 1) in puzzle.stars, True)
    self.assertEqual((0, 3) in puzzle.stars, True)
    self.assertEqual((3, 3) in puzzle.stars, True)

  def test_puzzle_gaps_expands(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".#...
#..#
....
#..#
""")
    stars = puzzle.expand(puzzle.stars)
    #
    #  .#vv.
    #  #.vv#
    #  vvvvv
    #  vvvvv
    #  #.vv#
    #
    self.assertEqual((1, 0) in stars, True)
    self.assertEqual((0, 1) in stars, True)
    self.assertEqual((4, 1) in stars, True)
    self.assertEqual((0, 4) in stars, True)
    self.assertEqual((4, 4) in stars, True)

  def test_puzzle_calculates_nearest_neighbour(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".#...
#..#
....
#..#
""")
    stars = puzzle.expand(puzzle.stars)
    nearest = puzzle.nearest(stars)
    self.assertEqual(nearest[stars[0]], stars[1])



if __name__ == '__main__':
    unittest.main()

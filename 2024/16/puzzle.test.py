import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_maze(self):
    puzzle = puz.Puzzle()
    puzzle.process("""#####
## E#
#S ##
#####
""")

    self.assertEqual(puzzle.width, 5)
    self.assertEqual(puzzle.height, 4)

    self.assertEqual(puzzle.at(1, 1), '#')
    self.assertEqual(puzzle.at(2, 2), ' ')

    self.assertEqual(puzzle.location, ((1, 2), 'E'))
    self.assertEqual(puzzle.end, (3, 1))

  def test_puzzle_finds_path_through_maze(self):
    puzzle = puz.Puzzle()
    puzzle.process("""#####
## E#
#S ##
#####
""")

    path = puzzle.find_path()

    self.assertEqual(path, [
      ((1,2), 'E', 0), ((2,2), 'E', 1), ((2,2), 'N', 1001),
      ((2,1), 'N', 1002), ((2,1), 'E', 2002), ((3,1), 'E', 2003)
    ])

  def test_puzzle_finds_all_best_paths_through_maze(self):
    puzzle = puz.Puzzle()
    puzzle.process("""#####
# E #    
# # #
#   #
##S##
#####
""")

    paths = puzzle.find_all_best_paths()
    self.assertEqual(len(paths), 2)

if __name__ == '__main__':
    unittest.main(verbosity=2)

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_lines(self):
    puzzle = puz.Puzzle()
    puzzle.process("""...S...
.......
...^...
.......
..^.^..
.......
""")


    self.assertEqual(puzzle.at(3,0), 'S')
    self.assertEqual(puzzle.at(1,1), '.')
    self.assertEqual(puzzle.at(2,4), '^')

  def test_puzzle_calculates_splits(self):
    puzzle = puz.Puzzle()
    puzzle.process("""...S...
.......
...^...
.......
..^.^..
.......
""")
  
    splits, beams = puzzle.calculate_splits()

    #puzzle.print_debug(beams)

    self.assertEqual(len(splits), 3)

  def test_puzzle_calculates_universes(self):
    puzzle = puz.Puzzle()
    puzzle.process("""...S...
.......
...^...
.......
..^.^..
.......
""")
  
    count = puzzle.calculate_universes()

    self.assertEqual(count, 4)

if __name__ == '__main__':
    unittest.main(verbosity=2)

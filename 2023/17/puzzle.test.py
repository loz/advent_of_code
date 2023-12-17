import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_map(self):
    puzzle = puz.Puzzle()
    puzzle.process("""123
456
789
""")
    self.assertEqual(puzzle.at(1,1), 5)
    self.assertEqual(puzzle.at(2,2), 9)

  def test_puzzle_neighbours_gives_options(self):
    puzzle = puz.Puzzle()
    puzzle.process("""123
456
789
""")
    nbrs = puzzle.neighbours(1,1)
    self.assertEqual(((0,1), (-1, 0)) in nbrs, True)
    self.assertEqual(((2,1), ( 1, 0)) in nbrs, True)
    self.assertEqual(((1,0), (0, -1)) in nbrs, True)
    self.assertEqual(((1,2), (0,  1)) in nbrs, True)



if __name__ == '__main__':
    unittest.main()

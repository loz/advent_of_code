import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_finds_shortest_path(self):
    puzzle = puz.Puzzle()
    puzzle.process("""122
122
111
""")
    path = puzzle.shortest_path()
    self.assertEqual(path, [(0,0), (0,1), (0, 2), (1,2), (2,2)])

if __name__ == '__main__':
    unittest.main()

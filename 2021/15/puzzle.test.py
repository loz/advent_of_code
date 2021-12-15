import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_finds_shortest_path(self):
    puzzle = puz.Puzzle()
    puzzle.process("""122
122
111
""")
    path, distance = puzzle.shortest_path()
    self.assertEqual(path, [(0,0), (0,1), (0, 2), (1,2), (2,2)])

  def test_puzzle_expands_map(self):
    puzzle = puz.Puzzle()
    puzzle.process("""122
122
111
""")
    puzzle.expand()
    print puzzle.to_str()
    self.assertEqual(puzzle.to_str(), """122233344455566
122233344455566
111222333444555
233344455566677
233344455566677
222333444555666
344455566677788
344455566677788
333444555666777
455566677788899
455566677788899
444555666777888
566677788899911
566677788899911
555666777888999
""")

if __name__ == '__main__':
    unittest.main()

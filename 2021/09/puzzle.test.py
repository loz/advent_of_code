import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_detects_lows(self):
    puzzle = puz.Puzzle()
    puzzle.process("""123
456
785
""")
    lows = puzzle.identify_lows()
    assert(((0,0),1) in lows)
    assert(((2,2),5) in lows)

  def test_puzzle_detects_lows_not_where_same(self):
    puzzle = puz.Puzzle()
    puzzle.process("""123
456
786
""")
    lows = puzzle.identify_lows()
    assert(((0,0),1) in lows)
    assert(((2,2),6) not in lows)

  def test_puzzle_sizes_basin(self):
    puzzle = puz.Puzzle()
    puzzle.process("""123
239
999
""")
    self.assertEqual(puzzle.size_basin(((0,0),1)), 5)

if __name__ == '__main__':
    unittest.main()

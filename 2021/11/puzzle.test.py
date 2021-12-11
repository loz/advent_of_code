import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_flashes_above_8(self):
    puzzle = puz.Puzzle()
    puzzle.process("""11111
19991
19191
19991
11111
""")
    flashes = puzzle.step()
    self.assertEqual(puzzle.to_str(), """34543
40004
50005
40004
34543
""")
    self.assertEqual(flashes, 9)

if __name__ == '__main__':
    unittest.main()

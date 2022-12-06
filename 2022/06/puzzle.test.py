import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_detects_marker(self):
    puzzle = puz.Puzzle()
    puzzle.process("""aabbccddefgh
""")
    self.assertEquals(puzzle.marker, 11)

if __name__ == '__main__':
    unittest.main()

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_lines(self):
    puzzle = puz.Puzzle()
    puzzle.process("""
""")
    self.assertEqual(puzzle.item, 'expected')

if __name__ == '__main__':
    unittest.main(verbosity=2)

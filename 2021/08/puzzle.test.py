import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_matches_1(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ab ab | ab
""")
    first = puzzle.outputs[0]
    self.assertEqual(first, [1])

  def test_puzzle_matches_4(self):
    puzzle = puz.Puzzle()
    puzzle.process("""abcd ab | abcd
""")
    first = puzzle.outputs[0]
    self.assertEqual(first, [4])

  def test_puzzle_matches_7(self):
    puzzle = puz.Puzzle()
    puzzle.process("""abc ab | abc
""")
    first = puzzle.outputs[0]
    self.assertEqual(first, [7])

  def test_puzzle_matches_8(self):
    puzzle = puz.Puzzle()
    puzzle.process("""abcdefg ab | abcdefg
""")
    first = puzzle.outputs[0]
    self.assertEqual(first, [8])

if __name__ == '__main__':
    unittest.main()

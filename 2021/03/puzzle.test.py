import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_counts_most_common(self):
    puzzle = puz.Puzzle()
    puzzle.process("""010110
111111
000000
""")
    #most common = 010110
    self.assertEqual(puzzle.gamma, 0b010110)

  def test_puzzle_counts_least_common(self):
    puzzle = puz.Puzzle()
    puzzle.process("""010110
111111
000000
""")
    #most common = 010110
    self.assertEqual(puzzle.epsilon, 0b101001)

if __name__ == '__main__':
    unittest.main()

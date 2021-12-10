import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_scores_matched_0(self):
    puzzle = puz.Puzzle()
    puzzle.process("""inputhere
""")
    score, autoscore = puzzle.check('<>')
    self.assertEqual(score, 0)

  def test_puzzle_scores_unmatched_3(self):
    puzzle = puz.Puzzle()
    puzzle.process("""inputhere
""")
    score, autoscore = puzzle.check('<><)')
    self.assertEqual(score, 3)

  def test_puzzle_scores_unmatched_57(self):
    puzzle = puz.Puzzle()
    puzzle.process("""inputhere
""")
    score, autoscore = puzzle.check('<>()(]')
    self.assertEqual(score, 57)

  def test_puzzle_scores_autocorrect(self):
    puzzle = puz.Puzzle()
    puzzle.process("""inputhere
""")
    score, autoscore = puzzle.check('<{([{{}}[<[[[<>{}]]]>[]]')
    self.assertEqual(autoscore, 294)

if __name__ == '__main__':
    unittest.main()

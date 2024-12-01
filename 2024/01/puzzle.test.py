import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_pairs_numbers(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1   2
""")
    self.assertEquals(puzzle.pair(0), (1,2))

  def test_puzzle_has_left_list(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1   2
3   4
""")
    self.assertEquals(puzzle.left_list(), [1, 3])

  def test_puzzle_has_right_list(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1   2
3   4
""")
    self.assertEquals(puzzle.right_list(), [2, 4])

  def test_puzzle_matches_smallest_pairs(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1   5
3   4
7   2
""")
    pairs = puzzle.match_smallest()
    self.assertEquals(pairs[0], (1,2))
    self.assertEquals(pairs[1], (3,4))
    self.assertEquals(pairs[2], (7,5))
    
  def test_puzzle_calculates_similarity_when_none(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1   5
3   4
7   2
""")
    self.assertEquals(puzzle.similarity(1), 0)

  def test_puzzle_calculates_similarity_when_none(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1   5
3   4
7   1
""")
    self.assertEquals(puzzle.similarity(1), 1)

if __name__ == '__main__':
    unittest.main()

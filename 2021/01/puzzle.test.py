import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_sliding_window(self):
    puzzle = puz.Puzzle()
    puzzle.process("""0
		1
		2
    3
""")
    self.assertEquals(puzzle.windows, [3, 6])

  def test_puzzle_counts_one_increment(self):
    puzzle = puz.Puzzle()
    puzzle.process("""0
		1
		0
""")
    puzzle.count_increments([0,1])
    self.assertEquals(puzzle.increments, 1)

  def test_puzzle_counts_a_later_increment(self):
    puzzle = puz.Puzzle()
    puzzle.process("""0
		1
		0
		1
		0
""")
    puzzle.count_increments([0,1,0,1])
    self.assertEquals(puzzle.increments, 2)

if __name__ == '__main__':
    unittest.main()

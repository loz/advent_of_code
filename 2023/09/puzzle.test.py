import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_numbers(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1 2 3 4 5 6 7
1 2 4 6 10 16
2 4 8 16 32 64
10 100 1000 10000
""")
    self.assertEquals(puzzle.readings[0], [1, 2, 3, 4, 5, 6, 7])

  def test_puzzle_reduces_a_line(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1 2 3 4 5 6 7
1 2 4 6 10 16
2 4 8 16 32 64
10 100 1000 10000
""")
    self.assertEquals(puzzle.reduce([1, 2, 3, 4, 5, 6, 7]), [1, 1, 1, 1, 1, 1])
    self.assertEquals(puzzle.reduce([1, 1, 1, 1, 1, 1]), [0, 0, 0, 0, 0])
    self.assertEquals(puzzle.reduce([10, 100, 1000, 10000]), [90, 900, 9000])

  def test_puzzle_generates_next_in_sequence(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1 2 3 4 5 6 7
0 2 4 6 10 16
2 4 8 16 32 64
10 100 1000 10000
""")
    self.assertEquals(puzzle.generate([1, 2, 3, 4, 5, 6, 7]), 8)
    self.assertEquals(puzzle.generate([0, 2, 6, 12, 20]), 30)

if __name__ == '__main__':
    unittest.main()

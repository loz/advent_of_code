import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_positive_move_forward(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1
2
3
4
5
6
""")
    self.assertEquals(puzzle.atindex(2).num, 3)
    puzzle.decrypt()
    self.assertEquals(puzzle.atindex(2).num, 4)

  def test_puzzle_moves_loop_round_forever(self):
    puzzle = puz.Puzzle()
    puzzle.process("""0
0
0
0
0
10
""")
    [0, 0, 0, 0, 0, 10]
    puzzle.decrypt()
    self.assertEquals(puzzle.atindex(5).num, 10)

  def test_puzzle_moves_negative_left(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1
2
-3
4
55
6
""")
    puzzle.decrypt()
    self.assertEquals(puzzle.atindex(3).num, -3)

if __name__ == '__main__':
    unittest.main()

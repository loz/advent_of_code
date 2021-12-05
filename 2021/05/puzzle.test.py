import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_draws_horiz_lines(self):
    puzzle = puz.Puzzle()
    puzzle.process("""0,0 -> 3,0
0,2 -> 2,2
2,0 -> 3,0
""")
    self.assertEqual(puzzle.to_str(4), """1122
....
111.
....
""")

  def test_puzzle_draws_vert_lines(self):
    puzzle = puz.Puzzle()
    puzzle.process("""0,0 -> 0,3
3,1 -> 3,2
0,2 -> 0,3
""")
    self.assertEqual(puzzle.to_str(4), """1...
1..1
2..1
2...
""")

  def test_puzzle_draws_calculate_danger(self):
    puzzle = puz.Puzzle()
    puzzle.process("""0,0 -> 0,3
3,1 -> 3,2
0,2 -> 0,3
""")
    self.assertEqual(puzzle.to_str(4), """1...
1..1
2..1
2...
""")
    self.assertEqual(puzzle.danger, 2)

if __name__ == '__main__':
    unittest.main()

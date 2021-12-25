import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_scans_map(self):
    puzzle = puz.Puzzle()
    puzzle.process("""v.>v
.>..
>...
""")
    self.assertEqual(puzzle.at(0,0), 'v')
    self.assertEqual(puzzle.at(2,0), '>')
    self.assertEqual(puzzle.at(0,2), '>')

  def test_puzzle_move_right_in_step(self):
    puzzle = puz.Puzzle()
    puzzle.process("""v.>v
.>..
>...
""")
    puzzle.step()
    self.assertEqual(puzzle.at(2,1), '>')
    self.assertEqual(puzzle.at(1,2), '>')

  def test_puzzle_move_down_in_step(self):
    puzzle = puz.Puzzle()
    puzzle.process("""v.>v
.>..
>...
""")
    puzzle.step()
    self.assertEqual(puzzle.at(0,1), 'v')
    self.assertEqual(puzzle.at(3,1), 'v')

  def test_puzzle_dont_move_if_blocked(self):
    puzzle = puz.Puzzle()
    puzzle.process("""v.>v
.>..
>...
""")
    puzzle.step()
    self.assertEqual(puzzle.at(2,0), '>')

  def test_puzzle_wrap_at_bounds(self):
    puzzle = puz.Puzzle()
    puzzle.process("""...>
....
.v..
""")
    puzzle.step()
    self.assertEqual(puzzle.at(0,0), '>')
    self.assertEqual(puzzle.at(1,0), 'v')

  def test_puzzle_horiz_move_before_vert(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".>v>
....
.v..
""")
    puzzle.step()
    self.assertEqual(puzzle.at(0,0), '>')
    self.assertEqual(puzzle.at(1,0), '>')
    self.assertEqual(puzzle.at(2,1), 'v')

if __name__ == '__main__':
    unittest.main()

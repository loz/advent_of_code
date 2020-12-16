import unittest
import puzzle as puz

EXAMPLE="""Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.
"""

class TestPuzzle(unittest.TestCase):

  def test_parses_positions(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)

    self.assertEqual(puzzle.position(0,1), 4)
    self.assertEqual(puzzle.position(0,2), 1)

  def test_position_at_time(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)

    self.assertEqual(puzzle.position(1,1), 0)
    self.assertEqual(puzzle.position(1,2), 0)

    self.assertEqual(puzzle.position(2,1), 1)
    self.assertEqual(puzzle.position(2,2), 1)

if __name__ == '__main__':
    unittest.main()

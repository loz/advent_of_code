import unittest
import puzzle as puz

EXAMPLE="""5 1 9 5
7 5 3
2 4 6 8
"""

class TestPuzzle(unittest.TestCase):

  def test_can_parse_values(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)

    self.assertEqual(puzzle.data[0], [5, 1, 9, 5])

  def test_can_checkline(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)

    self.assertEqual(puzzle.checkline([5, 1, 9, 5]), 8)

  def test_can_checkdivisor(self):
    puzzle = puz.Puzzle()

    self.assertEqual(puzzle.checkdivisor([5, 9, 2, 8]), 4)
    self.assertEqual(puzzle.checkdivisor([9, 4, 7, 3]), 3)
    self.assertEqual(puzzle.checkdivisor([3, 8, 6, 5]), 2)

if __name__ == '__main__':
    unittest.main()

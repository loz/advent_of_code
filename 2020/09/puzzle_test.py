import unittest
import puzzle as puz

INPUT="""35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
"""

class TestPuzzle(unittest.TestCase):

  def test_take_with_preamble_valid(self):
    puzzle = puz.Puzzle()
    puzzle.process(INPUT)
    n, isValid = puzzle.take(5)
    self.assertEqual(n, 40)
    self.assertTrue(isValid)

  def test_take_moves_cursor(self):
    puzzle = puz.Puzzle()
    puzzle.process(INPUT)
    n, isValid = puzzle.take(5)
    n, isValid = puzzle.take(5)
    self.assertEqual(n, 62)
    self.assertTrue(isValid)

  def test_take_with_preamble_invalid(self):
    puzzle = puz.Puzzle()
    puzzle.process(INPUT)
    n, isValid = puzzle.take(4)
    self.assertEqual(n, 47)
    self.assertFalse(isValid)

if __name__ == '__main__':
    unittest.main()

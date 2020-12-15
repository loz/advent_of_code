import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_speaks_numbers_given_first(self):
    puzzle = puz.Puzzle()
    puzzle.process("0,3,6")
    self.assertEqual(puzzle.next(), 0)
    self.assertEqual(puzzle.next(), 3)
    self.assertEqual(puzzle.next(), 6)

  def test_if_last_spoken_new_next_is_zero(self):
    puzzle = puz.Puzzle()
    puzzle.process("0,3,6")
    for i in range(3):
      puzzle.next()
    self.assertEqual(puzzle.next(), 0)

  def test_if_last_spoken_repeat_next_diffbetween_utterance(self):
    puzzle = puz.Puzzle()
    puzzle.process("0,3,6")
    self.assertEqual(puzzle.next(), 0)
    self.assertEqual(puzzle.next(), 3)
    self.assertEqual(puzzle.next(), 6)
    self.assertEqual(puzzle.next(), 0)
    self.assertEqual(puzzle.next(), 3)
    self.assertEqual(puzzle.next(), 3)
    self.assertEqual(puzzle.next(), 1)
    self.assertEqual(puzzle.next(), 0)
    self.assertEqual(puzzle.next(), 4)
    self.assertEqual(puzzle.next(), 0)

if __name__ == '__main__':
    unittest.main()

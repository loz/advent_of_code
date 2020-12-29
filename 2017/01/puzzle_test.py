import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_nomatch_0(self):
    puzzle = puz.Puzzle()
    puzzle.process1("1234")
    self.assertEqual(puzzle.value, 0)

  def test_match_pairs_counts(self):
    puzzle = puz.Puzzle()
    puzzle.process1("1122")
    self.assertEqual(puzzle.value, 3)

  def test_match_all_pairs(self):
    puzzle = puz.Puzzle()
    puzzle.process1("1111")
    self.assertEqual(puzzle.value, 4)

  def test_match_wraps(self):
    puzzle = puz.Puzzle()
    puzzle.process1("91212129")
    self.assertEqual(puzzle.value, 9)

  def test_match_oposites(self):
    puzzle = puz.Puzzle()
    puzzle.process("1212")
    self.assertEqual(puzzle.value, 6)
    puzzle.process("1221")
    self.assertEqual(puzzle.value, 0)
    puzzle.process("123425")
    self.assertEqual(puzzle.value, 4)
    puzzle.process("123123")
    self.assertEqual(puzzle.value, 12)
    puzzle.process("12131415")
    self.assertEqual(puzzle.value, 4)


if __name__ == '__main__':
    unittest.main()

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_nodigit_is_0(self):
    puzzle = puz.Puzzle()
    puzzle.process("""abc""")
    self.assertEquals(puzzle.total, 0)

  def test_puzzle_single_digit_double(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ab8c""")
    self.assertEquals(puzzle.total, 88)

  def test_puzzle_two_digits(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ab8sd4c""")
    self.assertEquals(puzzle.total, 84)

  def test_puzzle_multiple_digits(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ab1ss8ss9d4c""")
    self.assertEquals(puzzle.total, 14)

  def test_puzzle_one(self):
    puzzle = puz.Puzzle()
    puzzle.process("""aboness8ss9d4c""")
    self.assertEquals(puzzle.total, 14)

  def test_puzzle_two(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ab1ss8ss9dtwoc""")
    self.assertEquals(puzzle.total, 12)

  def test_puzzle_three(self):
    puzzle = puz.Puzzle()
    puzzle.process("""abthreess8ss9dtwoc""")
    self.assertEquals(puzzle.total, 32)

  def test_puzzle_four(self):
    puzzle = puz.Puzzle()
    puzzle.process("""abthreess8ss9dfour""")
    self.assertEquals(puzzle.total, 34)

  def test_puzzle_five(self):
    puzzle = puz.Puzzle()
    puzzle.process("""abfivess8ss9dfour""")
    self.assertEquals(puzzle.total, 54)

  def test_puzzle_six(self):
    puzzle = puz.Puzzle()
    puzzle.process("""absixss8ss9dfour""")
    self.assertEquals(puzzle.total, 64)

  def test_puzzle_seven(self):
    puzzle = puz.Puzzle()
    puzzle.process("""absevenss8ss9dfour""")
    self.assertEquals(puzzle.total, 74)

  def test_puzzle_eight(self):
    puzzle = puz.Puzzle()
    puzzle.process("""absevenss8ss9deightss""")
    self.assertEquals(puzzle.total, 78)

  def test_puzzle_nine(self):
    puzzle = puz.Puzzle()
    puzzle.process("""abniness8ss9deightss""")
    self.assertEquals(puzzle.total, 98)

  def test_puzzle_zero(self):
    puzzle = puz.Puzzle()
    puzzle.process("""abniness8ss9dzeross""")
    self.assertEquals(puzzle.total, 90)

  def test_puzzle_overlaps(self):
    puzzle = puz.Puzzle()
    puzzle.process("""abnineightss""")
    self.assertEquals(puzzle.total, 98)

if __name__ == '__main__':
    unittest.main()

import unittest
import puzzle as puz

EXAMPLE = """b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
"""

class TestPuzzle(unittest.TestCase):

  def test_inc_if_eq(self):
    puzzle = puz.Puzzle()
    puzzle.process("""b inc 5 if a == 1
b inc 5 if a == 0
""")
    puzzle.run()
    self.assertEqual(puzzle.get_reg('b'), 5)

  def test_dec_if_lt(self):
    puzzle = puz.Puzzle()
    puzzle.process("""b dec 5 if a < 0
b dec 5 if a < 1
""")
    puzzle.run()
    self.assertEqual(puzzle.get_reg('b'), -5)

  def test_inc_if_gt(self):
    puzzle = puz.Puzzle()
    puzzle.process("""b inc 5 if a > 1
b inc 5 if a > -1
""")
    puzzle.run()
    self.assertEqual(puzzle.get_reg('b'), 5)

  def test_dec_if_lteq(self):
    puzzle = puz.Puzzle()
    puzzle.process("""b dec 5 if a <= 0
b dec 5 if a <= -1
""")
    puzzle.run()
    self.assertEqual(puzzle.get_reg('b'), -5)

  def test_inc_if_gteq(self):
    puzzle = puz.Puzzle()
    puzzle.process("""b inc 5 if a >= 1
b inc 5 if a >= 0
""")
    puzzle.run()
    self.assertEqual(puzzle.get_reg('b'), 5)

  def test_dec_if_noteq(self):
    puzzle = puz.Puzzle()
    puzzle.process("""b dec 5 if a != 0
b dec 5 if a != -1
""")

    puzzle.run()
    self.assertEqual(puzzle.get_reg('b'), -5)
if __name__ == '__main__':
    unittest.main()

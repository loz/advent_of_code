import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_parses_depart_time(self):
    puzzle = puz.Puzzle()
    puzzle.process("""939
7,13,x,x,59,x,31,19
""")
    self.assertEqual(puzzle.depart, 939)

  def test_parses_busses(self):
    puzzle = puz.Puzzle()
    puzzle.process("""939
7,13,x,x,59,x,31,19
""")
    self.assertEqual(puzzle.busses, [7,13,59,31,19])

  def test_calc_next(self):
    puzzle = puz.Puzzle()
    puzzle.process("""939
7,13,x,x,59,x,31,19
""")
    self.assertEqual(puzzle.next(7), 945)
    self.assertEqual(puzzle.next(13), 949)
    self.assertEqual(puzzle.next(59), 944)
    self.assertEqual(puzzle.next(31), 961)
    self.assertEqual(puzzle.next(19), 950)

  def test_can_find_rem_factors(self):
    puzzle = puz.Puzzle()
    puzzle.process("""939
17,x,13,19
""")
    self.assertEqual(puzzle.remfactor(13), 7)
    self.assertEqual(puzzle.remfactor(19), 9)


# Common Factors Requirest
# 17,x,13,19
# N % 17 == 0
# (N + 2) % 13 == 0
# (N + 3) % 19 == 0
# or
# N % 17 == 0
# N % 13 == 11
# N % 19 == 16
#


if __name__ == '__main__':
    unittest.main()

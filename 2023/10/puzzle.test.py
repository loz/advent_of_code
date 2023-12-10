import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_finds_the_start(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".F-S.
.|.|.
.L.J.
""")

    self.assertEqual(puzzle.start, (3,0))

  def test_puzzle_identifies_if_start_is_TR_corner(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".F-S.
.|.|.
.L-J.
""")
    self.assertEqual(puzzle.at(3,0), '7')

  def test_puzzle_identifies_if_start_is_T(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".FS7.
.|.|.
.L-J.
""")
    self.assertEqual(puzzle.at(2,0), '-')

  def test_puzzle_identifies_if_start_is_TL(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".S-7.
.|.|.
.L-J.
""")
    self.assertEqual(puzzle.at(1,0), 'F')

  def test_puzzle_identifies_if_start_is_L(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".F-7.
.S.|.
.L-J.
""")
    self.assertEqual(puzzle.at(1,1), '|')

  def test_puzzle_identifies_if_start_is_BL(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".F-7.
.|.|.
.S-J.
""")
    self.assertEqual(puzzle.at(1,2), 'L')

  def test_puzzle_identifies_if_start_is_B(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".F-7.
.|.|.
.LSJ.
""")
    self.assertEqual(puzzle.at(2,2), '-')

  def test_puzzle_identifies_if_start_is_BR(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".F-7.
.|.|.
.L-S.
""")
    self.assertEqual(puzzle.at(3,2), 'J')

  def test_puzzle_identifies_if_start_is_R(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".F-7.
.|.S.
.L-J.
""")
    self.assertEqual(puzzle.at(3,1), '|')

  def test_puzzle_traces_loop(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".S-7.
.|.|.
.L-J.
""")
    loop, lmap = puzzle.trace_loop()
    self.assertEqual((1, 0) in loop, True)
    self.assertEqual((2, 0) in loop, True)
    self.assertEqual((3, 0) in loop, True)
    self.assertEqual((3, 1) in loop, True)
    self.assertEqual((3, 2) in loop, True)
    self.assertEqual((2, 2) in loop, True)
    self.assertEqual((1, 2) in loop, True)
    self.assertEqual((1, 1) in loop, True)

if __name__ == '__main__':
    unittest.main()

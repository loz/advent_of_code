import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_cpy(self):
    puzzle = puz.Puzzle()
    puzzle.process("""cpy 41 a
cpy 21 b
""")
    puzzle.run()
    self.assertEqual(puzzle.reg['a'], 41)
    self.assertEqual(puzzle.reg['b'], 21)

  def test_inc(self):
    puzzle = puz.Puzzle()
    puzzle.process("""inc a
inc c
""")
    puzzle.run()
    self.assertEqual(puzzle.reg['a'], 1)
    self.assertEqual(puzzle.reg['c'], 1)

  def test_dec(self):
    puzzle = puz.Puzzle()
    puzzle.process("""dec a
dec b
""")
    puzzle.run()
    self.assertEqual(puzzle.reg['a'], -1)
    self.assertEqual(puzzle.reg['b'], -1)

  def test_dec(self):
    puzzle = puz.Puzzle()
    puzzle.process("""jnz a 2
cpy 2 b
dec b
jnz b -1
""")
    puzzle.run()
    self.assertEqual(puzzle.reg['a'], 0)
    self.assertEqual(puzzle.reg['b'], 0)

if __name__ == '__main__':
    unittest.main()

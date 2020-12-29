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
      
  def test_tgl(self):
    puzzle = puz.Puzzle()
    puzzle.process("""cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a
tgl 1
jnz 1 1
tgl 10
tgl 1
inc a
tgl 1
dec a
""")
    puzzle.run()
    self.assertEqual(puzzle.instructions[3], ['inc', 'a'])
    self.assertEqual(puzzle.instructions[4], ['jnz', '1', 'a'])
    self.assertEqual(puzzle.instructions[8], ['cpy', '1', '1'])
    self.assertEqual(puzzle.instructions[11],['dec', 'a'])
    self.assertEqual(puzzle.instructions[13], ['inc', 'a'])

  def test_out(self):
    puzzle = puz.Puzzle()
    puzzle.process("""cpy 2 a
out 12
out a
out 10
""")
    output = puzzle.run()
    self.assertEqual(output, [12, 2, 10])

if __name__ == '__main__':
    unittest.main()

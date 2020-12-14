import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_mask_bits(self):
    puzzle = puz.Puzzle()
    puzzle.process("""mask = XXXX""")
    self.assertEqual(puzzle.mask, ['X', 'X', 'X', 'X'])

  def test_mask_mem_write(self):
    puzzle = puz.Puzzle()
    puzzle.process("""mask = X1X0
mem[8] = 3
""")
    self.assertEqual(puzzle.memory[8], 6)

  def test_mask_set_multiple(self):
    puzzle = puz.Puzzle()
    puzzle.process("""mask = X1X0
mem[8] = 3
mask = 11XX
mem[10] = 3
""")
    self.assertEqual(puzzle.memory[10], 15)



if __name__ == '__main__':
    unittest.main()

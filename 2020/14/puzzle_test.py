import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_mask_bits(self):
    puzzle = puz.Puzzle()
    puzzle.process("""mask = XXXX""")
    self.assertEqual(puzzle.mask, ['X', 'X', 'X', 'X'])

  def test_mask_mem_write(self):
    puzzle = puz.Puzzle()
    puzzle.process("""mask = X100
mem[8] = 3
""")
    # mem = 1000
    # msk = X100
    # res = X100 
    # locs = 0100, 1100 
    #        4     12  
    self.assertEqual(puzzle.memory[4],  3)
    self.assertEqual(puzzle.memory[12], 3)

  def test_mask_set_multiple(self):
    puzzle = puz.Puzzle()
    puzzle.process("""mask = X100
mem[8] = 3
mask = 1X0X
mem[10] = 9
""")
    # mem = 1010
    # msk = 1X0X
    # res = 1X1X 
    # locs = 1010, 1011, 1110, 1111
    #        10    11    14    15
    self.assertEqual(puzzle.memory[10], 9)
    self.assertEqual(puzzle.memory[11], 9)
    self.assertEqual(puzzle.memory[14], 9)
    self.assertEqual(puzzle.memory[15], 9)



if __name__ == '__main__':
    unittest.main()

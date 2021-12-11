import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_fast_calculate(self):
    puzzle = puz.Puzzle()
    fast3 = puzzle.fast(3, 2017)
    fast324 = puzzle.fast(324, 2017)
    self.assertEqual(fast3, 1226)
    self.assertEqual(fast324, 243)
    
  def test_puzzle_spins_1_correctly(self):
    puzzle = puz.Puzzle()
    puzzle.spinlock(3)
    self.assertEqual(puzzle.position, 1)
    self.assertEqual(puzzle.buffer, [0, 1])

  def test_puzzle_spins_2_correctly(self):
    puzzle = puz.Puzzle()
    puzzle.spinlock(3)
    puzzle.spinlock(3)
    self.assertEqual(puzzle.position, 1)
    self.assertEqual(puzzle.buffer, [0, 2, 1])

  def test_puzzle_spins_3_correctly(self):
    puzzle = puz.Puzzle()
    puzzle.spinlock(3)
    puzzle.spinlock(3)
    puzzle.spinlock(3)
    self.assertEqual(puzzle.position, 2)
    self.assertEqual(puzzle.buffer, [0, 2, 3, 1])

if __name__ == '__main__':
    unittest.main()

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_default_range_allow(self):
    puzzle = puz.Puzzle(9)
    for i in range(9):
      self.assertTrue(puzzle.valid(i))

  def test_ranges_blocked(self):
    puzzle = puz.Puzzle(9)
    puzzle.process("4-7")
    self.assertFalse(puzzle.valid(5))
    self.assertTrue(puzzle.valid(3))
    self.assertTrue(puzzle.valid(8))

  def test_blocks_overlaps_end(self):
    puzzle = puz.Puzzle(9)
    puzzle.process("""4-7
 5-8
 """)
    self.assertFalse(puzzle.valid(8))
    self.assertTrue(puzzle.valid(3))
    self.assertTrue(puzzle.valid(9))

  def test_blocks_overlaps_start(self):
    puzzle = puz.Puzzle(9)
    puzzle.process("""4-7
 2-5
 """)
    self.assertFalse(puzzle.valid(2))
    self.assertFalse(puzzle.valid(5))
    self.assertTrue(puzzle.valid(1))
    self.assertTrue(puzzle.valid(8))
    
  def test_blocks_wraps_both(self):
    puzzle = puz.Puzzle(9)
    puzzle.process("""5-6
 4-7
 """)
    self.assertFalse(puzzle.valid(4))
    self.assertFalse(puzzle.valid(5))
    self.assertFalse(puzzle.valid(7))
    self.assertTrue(puzzle.valid(3))
    self.assertTrue(puzzle.valid(8))

  def test_blocks_matches_exact_open_ranges(self):
    puzzle = puz.Puzzle(9)
    print '='*10
    puzzle.process("""3-4
 7-8
 5-6
 """)
    print 'RANGES', puzzle.ranges
    self.assertFalse(puzzle.valid(3))
    self.assertFalse(puzzle.valid(8))
    self.assertTrue(puzzle.valid(2))
    self.assertTrue(puzzle.valid(9))

if __name__ == '__main__':
    unittest.main()

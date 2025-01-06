import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_schematics_for_a_lock(self):
    puzzle = puz.Puzzle()
    puzzle.process("""#####
###.#
#.#.#
#...#
#...#
#....
.....

.....
#..#.
#..#.
#.##.
#.##.
#####
#####
""")
    self.assertEqual(len(puzzle.locks), 1)
    self.assertIn( (5,1,2,0,4), puzzle.locks)

  def test_puzzle_parses_schematics_for_a_key(self):
    puzzle = puz.Puzzle()
    puzzle.process("""#####
###.#
#.#.#
#...#
#...#
#....
.....

.....
#..#.
#..#.
#.##.
#.##.
#####
#####
""")
    self.assertEqual(len(puzzle.keys), 1)
    self.assertIn( (5,1,3,5,1), puzzle.keys)

  def test_key_does_not_fit_lock_when_overlap(self):
    puzzle = puz.Puzzle()

    lock = (0,5,3,4,3)
    key = (5,0,2,1,3)
    self.assertFalse(puzzle.fits(lock, key))

  def test_key_does_fit_when_does_not_overlap_lock(self):
    puzzle = puz.Puzzle()

    lock = (0,5,3,4,3)
    key = (3,0,2,0,1)
    self.assertTrue(puzzle.fits(lock, key))
    
if __name__ == '__main__':
    unittest.main(verbosity=2)

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_lines(self):
    puzzle = puz.Puzzle()
    puzzle.process("""..@@.
.@@..
..@.@
.@.@@
""")

    self.assertEqual(puzzle.at(0,0), '.')
    self.assertEqual(puzzle.at(2,2), '@')


  def test_puzzle_scans_accessible(self):
    puzzle = puz.Puzzle()
    puzzle.process("""..@@.
.@@@.
..@.@
.@.@@
""")

    accessible = puzzle.scan_accessible()
    puzzle.print_debug(accessible)

    #{(4, 3), (1, 1), (4, 2), (3, 0), (3, 3), (1, 3)}
    self.assertIn((1,1), accessible)
    self.assertIn((1,3), accessible)
    self.assertIn((3,0), accessible)
    self.assertIn((3,3), accessible)
    self.assertIn((4,2), accessible)
    self.assertIn((4,2), accessible)



if __name__ == '__main__':
    unittest.main(verbosity=2)

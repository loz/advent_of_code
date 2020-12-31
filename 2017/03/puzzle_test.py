import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_can_calc_xy_of_odd_squares(self):
    puzzle = puz.Puzzle()
   
    self.assertEqual(puzzle.loc(1),  (0,0))
    self.assertEqual(puzzle.loc(9),  (1,1))
    self.assertEqual(puzzle.loc(25), (2,2))

  def test_can_calc_xy_of_even_squares(self):
    puzzle = puz.Puzzle()
   
    self.assertEqual(puzzle.loc(4),  (0,-1))
    self.assertEqual(puzzle.loc(16), (-1,-2))
    self.assertEqual(puzzle.loc(36), (-2,-3))

  def test_can_calc_xy_of_non_squares(self):
    puzzle = puz.Puzzle()
   
    self.assertEqual(puzzle.loc(2),  (1, 0))
    self.assertEqual(puzzle.loc(20), (-2,1))
    self.assertEqual(puzzle.loc(23), (0,2))
    self.assertEqual(puzzle.loc(13), (2,-2))
    self.assertEqual(puzzle.loc(33), (1,-3))

if __name__ == '__main__':
    unittest.main()

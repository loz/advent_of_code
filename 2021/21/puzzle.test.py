import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_calcs_space_for_move(self):
    puzzle = puz.Puzzle()
    space = 4
    player = 1
    self.assertEqual(puzzle.calc_space(space, player, 1), 10)
    space = 6
    self.assertEqual(puzzle.calc_space(space, player, 4), 6)

    space = 6
    player = 2
    self.assertEqual(puzzle.calc_space(space, player, 3), 7)
    pass

if __name__ == '__main__':
    unittest.main()

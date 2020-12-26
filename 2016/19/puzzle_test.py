import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_inits_with_elves(self):
    puzzle = puz.Puzzle()
    puzzle.process(5)
    
    self.assertEqual(puzzle.game[1], 1)
    self.assertEqual(puzzle.game[2], 1)
    self.assertEqual(puzzle.game[3], 1)
    self.assertEqual(puzzle.game[4], 1)
    self.assertEqual(puzzle.game[5], 1)

  def test_can_play_game(self):
    puzzle = puz.Puzzle()
    puzzle.process(5)

    winner = puzzle.play_game()

    self.assertEqual(winner, 3)

  def test_can_play_game2(self):
    puzzle = puz.Puzzle()
    puzzle.process(5)

    winner = puzzle.play_game2()

    self.assertEqual(winner, 2)


if __name__ == '__main__':
    unittest.main()

import unittest
import puzzle as puz

INPUT = [3, 8, 9, 1, 2, 5, 4, 6, 7]

class TestPuzzle(unittest.TestCase):

  def test_play_move(self):
    puzzle = puz.Puzzle()
    cups = puzzle.play(INPUT)
    self.assertEqual(cups, [2, 8, 9, 1, 5, 4, 6, 7, 3])

  def test_play_move_when_dest_picked(self):
    puzzle = puz.Puzzle()
    cups = puzzle.play(INPUT)
    cups = puzzle.play(cups)
    self.assertEqual(cups, [5, 4, 6, 7, 8, 9, 1, 3, 2])

if __name__ == '__main__':
    unittest.main()

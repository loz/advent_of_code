import unittest
import puzzle as puz

EXAMPLE="389125467"

class TestPuzzle(unittest.TestCase):

  def test_play_move(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)
    puzzle.play()
    self.assertEqual(puzzle.head, 2)
    cups = puzzle.trace(9)
    self.assertEqual(cups, [2, 8, 9, 1, 5, 4, 6, 7, 3])

  def test_play_move_when_dest_picked(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)
    print puzzle.trace(9)
    puzzle.play()
    print puzzle.trace(9)
    puzzle.play()
    cups = puzzle.trace(9)
    self.assertEqual(cups, [5, 4, 6, 7, 8, 9, 1, 3, 2])

if __name__ == '__main__':
    unittest.main()

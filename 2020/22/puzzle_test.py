import unittest
import puzzle as puz

EXAMPLE = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
"""

class TestPuzzle(unittest.TestCase):

  def test_process_deck(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)

    self.assertEqual(puzzle.player[0], [9, 2, 6, 3, 1])
    self.assertEqual(puzzle.player[1], [5,8,4,7,10])

  def test_play_round(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)

    winner = puzzle.play_round()
    self.assertEqual(winner, 0)
    self.assertEqual(puzzle.player[0], [2, 6, 3, 1, 9, 5])
    self.assertEqual(puzzle.player[1], [8, 4, 7, 10])

  def test_play_recurisve_combat_recurse_winner(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)

    p1deck = [2, 8, 10]
    p2deck = [3, 4, 5, 6]
    """
p1: 2 8 10
p2: 3 4 5 6
R---
  p1 8 10
  p2 4 5 6
  - p1: 10 8 4
  - p2: 5 6
  - p1: 8 4 10 5
  - p2: 6
  - p1: 4 10 5 6 8 [wins]
- p1: 8 10 2 3
- p2: 4 5 6
- p1: 10 2 3 8 4
- p2: 5 6
- p1: 2 3 8 4 10 5
- p2: 6
- p1: 3 8 4 10 5
- p2: 6 2
- p1: 8 4 10 5
- p2: 2 6 3
- p1: 4 10 5 8 2
- p2: 6 3
- p1: 10 5 8 2
- p2: 3 6 4
- p1: 5 8 2 10 3
- p2: 6 4
- p1: 8 2 10 3
- p2: 4 6 5
- p1: 2 10 3 8 4
- p2: 6 5
- p1: 10 3 8 4
- p2: 5 6 2
- p1: 3 8 4 10 5 RECURSION - P1 Wins
- p2: 6 2
"""
    winner, p1deck, p2deck = puzzle.play_recursive_combat(p1deck, p2deck)
    self.assertEqual(winner, 0)
    self.assertEqual(p1deck, [3, 8, 4, 10, 5])
    self.assertEqual(p2deck, [6, 2])


if __name__ == '__main__':
    unittest.main()

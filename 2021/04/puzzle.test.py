import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_calls(self):
    puzzle = puz.Puzzle()
    puzzle.process("""2,5,6,7,12,32,67

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6
""")
    self.assertEqual(puzzle.calls, [2,5,6,7,12,32,67])

  def test_puzzle_parses_boards(self):
    puzzle = puz.Puzzle()
    puzzle.process("""2,5,6,7,12,32,67

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

33 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 61 12  6
""")
    self.assertEqual(puzzle.boards[0][0],[3, 15, 0, 2, 22])
    self.assertEqual(puzzle.boards[0][4],[14,21,16,12,6])
    self.assertEqual(puzzle.boards[1][0],[33, 15, 0, 2, 22])
    self.assertEqual(puzzle.boards[1][4],[14,21,61,12,6])

  def test_puzzle_game_wins_with_row(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1,12,20,15,19,3,9,19,20,14

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19
""")
    puzzle.play_bingo()
    self.assertEqual(puzzle.winning_board, 1)
    self.assertEqual(puzzle.last_call, 19)

  def test_puzzle_game_wins_with_colum(self):
    puzzle = puz.Puzzle()
    puzzle.process("""3,9,19,20,14,1,12,20,15,19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19
""")
    puzzle.play_bingo()
    self.assertEqual(puzzle.winning_board, 0)
    self.assertEqual(puzzle.last_call, 14)

  def test_puzzle_game_calculates_score(self):
    puzzle = puz.Puzzle()
    puzzle.process("""3,9,19,20,14,1,12,20,15,19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19
""")
    puzzle.play_bingo()
    self.assertEqual(puzzle.winning_score, 14 * (15+2+22+18+13+17+5+8+7+25+23+11+10+24+4+21+16+12+6))

if __name__ == '__main__':
    unittest.main()

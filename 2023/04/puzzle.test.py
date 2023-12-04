import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_cards(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
""")
    card = puzzle.cards[0]
    self.assertEqual(card, (2, [13,32,20,16,61], [61,30,68,82,17,32,24,19]))

  def test_puzzle_no_match_0_points(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Card 2: 13 32 20 16 61 |  1 30 68 82 17 31 24 19
""")
    card = puzzle.cards[0]
    self.assertEqual(puzzle.score(card), 0)

  def test_puzzle_1_match_1_points(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Card 2: 13 32 20 16 61 |  1 32 68 82 17 31 24 19
""")
    card = puzzle.cards[0]
    self.assertEqual(puzzle.score(card), 1)

  def test_puzzle_3_match_8_points(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Card 2: 13 32 20 16 61 |  1 32 68 20 17 31 61 19
""")
    card = puzzle.cards[0]
    self.assertEqual(puzzle.score(card), 4)

  def test_puzzle_card_wins_points_copies(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
""")
    card = puzzle.cards[0]
    expected = [puzzle.cards[1], puzzle.cards[2], puzzle.cards[3], puzzle.cards[4]]
    self.assertEqual(puzzle.winnings(card), expected)

if __name__ == '__main__':
    unittest.main()

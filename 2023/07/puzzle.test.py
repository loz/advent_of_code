import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_hands_and_bids(self):
    puzzle = puz.Puzzle()
    puzzle.process("""AAAKK 123
113Q1 456
""")
    self.assertEqual(puzzle.turns[0], ('AAAKK', 123))
    self.assertEqual(puzzle.turns[1], ('113Q1', 456))


  def test_puzzle_5ofkind_scores_highest(self):
    puzzle = puz.Puzzle()
    puzzle.process("""AAAKK 123
113Q1 456
""")
    self.assertEqual(puzzle.score('AAAAA'), 7)

  def test_puzzle_4ofkind_scores_next(self):
    puzzle = puz.Puzzle()
    puzzle.process("""AAAKK 123
113Q1 456
""")
    self.assertEqual(puzzle.score('AAAAQ'), 6)

  def test_puzzle_full_house_scores_next(self):
    puzzle = puz.Puzzle()
    puzzle.process("""AAAKK 123
113Q1 456
""")
    self.assertEqual(puzzle.score('AQAAQ'), 5)

  def test_puzzle_3_of_a_kind_scores_next(self):
    puzzle = puz.Puzzle()
    puzzle.process("""AAAKK 123
113Q1 456
""")
    self.assertEqual(puzzle.score('A1A2A'), 4)

  def test_puzzle_2_pair_scores_next(self):
    puzzle = puz.Puzzle()
    puzzle.process("""AAAKK 123
113Q1 456
""")
    self.assertEqual(puzzle.score('A1A21'), 3)

  def test_puzzle_1_pair_scores_next(self):
    puzzle = puz.Puzzle()
    puzzle.process("""AAAKK 123
113Q1 456
""")
    self.assertEqual(puzzle.score('A1A23'), 2)

  def test_puzzle_high_card_scores_last(self):
    puzzle = puz.Puzzle()
    puzzle.process("""AAAKK 123
113Q1 456
""")
    self.assertEqual(puzzle.score('A1K23'), 1)

  def test_puzzle_jokers_are_wild(self):
    puzzle = puz.Puzzle()
    puzzle.process("""AAAKK 123
113Q1 456
""")
    self.assertEqual(puzzle.wild_score('12345'), puzzle.score('12345'))  
    self.assertEqual(puzzle.wild_score('AAJJA'), puzzle.score('AAAAA'))
    self.assertEqual(puzzle.wild_score('KTJJT'), puzzle.score('KTTTT'))  
    self.assertEqual(puzzle.wild_score('KKJTT'), puzzle.score('KKKTT'))  
    self.assertEqual(puzzle.wild_score('KKJ12'), puzzle.score('KKK12'))  
    self.assertEqual(puzzle.wild_score('1234J'), puzzle.score('12344'))  
    self.assertEqual(puzzle.wild_score('T55J5'), puzzle.score('T5555'))  


  def test_puzzle_cmp_same_rank_on_cardorder_value(self):
    puzzle = puz.Puzzle()
    puzzle.process("""AAAKK 123
113Q1 456
""")
    self.assertEqual(puz.Puzzle.cmp_hand('AAAAK', 'KAAAA'), 1)
    self.assertEqual(puz.Puzzle.cmp_hand('KAAAK', 'KKAAA'), 1)
    self.assertEqual(puz.Puzzle.cmp_hand('QQKQK', 'KKAAA'), -1)
    self.assertEqual(puz.Puzzle.cmp_hand('AAAA2', 'AAAAK'), -1)

if __name__ == '__main__':
    unittest.main()

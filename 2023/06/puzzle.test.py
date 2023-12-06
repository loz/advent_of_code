import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_race_records(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Time:      10  20   30
Distance:  100  40  290
""")
  
    self.assertEqual(puzzle.records[0], (10, 100))
    self.assertEqual(puzzle.records[1], (20, 40))
    self.assertEqual(puzzle.records[2], (30, 290))

  def test_puzzle_calculates_distance_for_press_with_time(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Time:      10  20   30
Distance:  100  40  290
""")
  
    self.assertEqual(puzzle.calculate_distance(0, 10), 0)
    self.assertEqual(puzzle.calculate_distance(1, 10), 9)
    self.assertEqual(puzzle.calculate_distance(2, 10), 16)
    self.assertEqual(puzzle.calculate_distance(3, 10), 21)
    self.assertEqual(puzzle.calculate_distance(4, 10), 24)
    self.assertEqual(puzzle.calculate_distance(5, 10), 25)
    self.assertEqual(puzzle.calculate_distance(6, 10), 24)
    self.assertEqual(puzzle.calculate_distance(7, 10), 21)
    self.assertEqual(puzzle.calculate_distance(8, 10), 16)
    self.assertEqual(puzzle.calculate_distance(9, 10), 9)
    self.assertEqual(puzzle.calculate_distance(10, 10), 0)


  def test_puzzle_optimised_wincount_matches_brute_calc(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Time:      10  20   30
Distance:  100  40  290
""")

    self.assertEqual(puzzle.brute_wincount(7,9), puzzle.wincount(7,9))
    self.assertEqual(puzzle.brute_wincount(15,40), puzzle.wincount(15,40))
    self.assertEqual(puzzle.brute_wincount(30,200), puzzle.wincount(30,200))
    self.assertEqual(puzzle.brute_wincount(71530,940200), puzzle.wincount(71530,940200))
  
if __name__ == '__main__':
    unittest.main()

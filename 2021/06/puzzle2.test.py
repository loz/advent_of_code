import unittest
import puzzle2 as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_internal_timers_count_down(self):
    puzzle = puz.Puzzle()
    puzzle.process("""4,3,2
""")
    puzzle.tick()
    self.assertEqual(puzzle.state,[3,2,1])

  def test_puzzle_internal_zero_spawns_and_moves_to_six(self):
    puzzle = puz.Puzzle()
    puzzle.process("""0
""")
    puzzle.tick()
    self.assertEqual(puzzle.state,[6,8])

  def test_puzzle_calculate_growth_for_one_fish(self):
    puzzle = puz.Puzzle()
    puzzle.process("""0
""")
    growth = puzzle.calculate_growth(8,80)
    self.assertEqual(growth, 768)
    

if __name__ == '__main__':
    unittest.main()

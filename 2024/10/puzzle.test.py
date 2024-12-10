import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_topography(self):
    puzzle = puz.Puzzle()
    puzzle.process("""0123
7654
8900
""")
    self.assertEqual(puzzle.map[0][0], 0)
    self.assertEqual(puzzle.map[2][1], 9)
    self.assertEqual(puzzle.map[1][2], 5)
    self.assertEqual(puzzle.map[2][3], 0)

  def test_puzzle_finds_no_trail_when_no_move_possible(self):
    puzzle = puz.Puzzle()
    puzzle.process("""0123
7654
8900
""")
    
    trails = puzzle.find_trails((3, 2))
    self.assertEqual(trails, [])
    
  def test_puzzle_finds_trail(self):
    puzzle = puz.Puzzle()
    puzzle.process("""0123
7654
8900
""")
    
    trails = puzzle.find_trails((0, 0))
    self.assertEqual(len(trails), 1)
    self.assertEqual(trails[0], [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (2, 1), (1, 1), (0, 1), (0, 2), (1, 2)])

  def test_puzzle_finds_trailheads(self):
    puzzle = puz.Puzzle()
    puzzle.process("""0123
7654
8900
""")
    
    trailheads = puzzle.find_trailheads()
    self.assertEqual(len(trailheads), 3)
    self.assertIn((0,0), trailheads)
    self.assertIn((2,2), trailheads)
    self.assertIn((3,2), trailheads)

if __name__ == '__main__':
    unittest.main(verbosity=2)

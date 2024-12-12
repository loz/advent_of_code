import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_map(self):
    puzzle = puz.Puzzle()
    puzzle.process("""AABB
ABBC
CCCC
""")

    self.assertEqual(puzzle.at(0,0), 'A')
    self.assertEqual(puzzle.at(2,2), 'C')
    self.assertEqual(puzzle.at(2,1), 'B')

  def test_puzzle_scans_regions(self):
    puzzle = puz.Puzzle()
    puzzle.process("""AABB
ABBC
CCCC
""")

    regions = puzzle.region('A')

    self.assertEqual(len(regions), 1)
    self.assertEqual(len(regions[0]), 3)
    self.assertIn((0,0), regions[0])
    self.assertIn((0,1), regions[0])
    self.assertIn((1,0), regions[0])

  def test_puzzle_scans_contiguous_regions(self):
    puzzle = puz.Puzzle()
    puzzle.process("""AABB
ABBC
CCAA
""")

    regions = puzzle.region('A')

    self.assertEqual(len(regions), 2)
    self.assertEqual(len(regions[0]), 3)
    self.assertEqual(len(regions[1]), 2)

  def test_puzzle_calulates_areas_and_perimeters(self):
    puzzle = puz.Puzzle()
    puzzle.process("""AABB
ABBC
CCAA
""")

    regions = puzzle.region('B')
    self.assertEqual(len(regions), 1)
    region = regions[0]
    
    area, perim = puzzle.calculate_size(region)
    self.assertEqual(area, 4)
    self.assertEqual(perim, 10)

  def test_puzzle_calulates_areas_and_edges(self):
    puzzle = puz.Puzzle()
    puzzle.process("""AABB
ABBC
CCAA
""")

    regions = puzzle.region('A')
    self.assertEqual(len(regions), 2)
    region = regions[0]
    
    area, edges = puzzle.calculate_edge(region)
    self.assertEqual(area, 3)
    self.assertEqual(edges, 6)

  def test_puzzle_calulates_edges_for_bug_properly(self):
    puzzle = puz.Puzzle()
    puzzle.process("""......
.AAA..
.A.A..
.AA...
......
""")

    regions = puzzle.region('A')
    self.assertEqual(len(regions), 1)
    region = regions[0]
    
    area, edges = puzzle.calculate_edge(region)
    self.assertEqual(area, 7)
    self.assertEqual(edges, 10)

  def test_puzzle_calulates_edges_for_internal_properly(self):
    puzzle = puz.Puzzle()
    puzzle.process("""AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
""")

    regions = puzzle.region('A')
    region = regions[0]
    area, edges = puzzle.calculate_edge(region)
    self.assertEqual(edges, 12)


if __name__ == '__main__':
    unittest.main(verbosity=2)

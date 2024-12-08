import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_map_bounds(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".....
.3...
v....
.3.v.
..x..
.....
""")
    
    self.assertEqual(puzzle.map_width, 4)
    self.assertEqual(puzzle.map_height, 5)

  def test_puzzle_parses_antenna(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".....
.3...
v....
.3.v.
..x..
""")
    
    self.assertEqual(len(puzzle.antenae.keys()), 3)
    self.assertIn((1, 1), puzzle.antenae['3'])
    self.assertIn((1, 3), puzzle.antenae['3'])
    self.assertIn((0, 2), puzzle.antenae['v'])
    self.assertIn((3, 3), puzzle.antenae['v'])
    self.assertIn((2, 4), puzzle.antenae['x'])

  def test_puzzle_calculates_antinodes(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".....
.....
.a...
..a..
.....
""")
    
    antinodes = puzzle.antinodes('a')
    self.assertEqual(len(antinodes), 2)
    self.assertIn((0,1), antinodes)
    self.assertIn((3,4), antinodes)

  def test_puzzle_calculates_forward_slant_antinodes(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".....
.....
..x..
.x...
.....
""")
    
    antinodes = puzzle.antinodes('x')
    self.assertEqual(len(antinodes), 2)
    self.assertIn((0,4), antinodes)
    self.assertIn((3,1), antinodes)

  def test_puzzle_calculates_all_antinodes(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".....
.....
..e..
.ee..
.....
""")
    
    antinodes = puzzle.antinodes('e')
    self.assertEqual(len(antinodes), 6)
    self.assertIn((0,4), antinodes)
    self.assertIn((3,1), antinodes)
    self.assertIn((2,1), antinodes)
    self.assertIn((2,4), antinodes)
    self.assertIn((0,3), antinodes)
    self.assertIn((3,3), antinodes)

  def test_puzzle_excludes_out_of_bounds(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".....
.....
.b...
.h.h.
..b..
""")
    
    antinodes = puzzle.antinodes('b')
    self.assertEqual(len(antinodes), 1)
    self.assertIn((0,0), antinodes)
    antinodes = puzzle.antinodes('h')
    self.assertEqual(len(antinodes), 0)

  def test_puzzle_calculates_all_resonant_antinodes(self):
    puzzle = puz.Puzzle()
    puzzle.process("""........
........
........
........
...r....
....r...
........
........
""")
    
    antinodes = puzzle.resonant_antinodes('r')
    self.assertEqual(len(antinodes), 5)
    self.assertIn((2,3), antinodes)
    self.assertIn((1,2), antinodes)
    self.assertIn((0,1), antinodes)

    self.assertIn((5,6), antinodes)
    self.assertIn((6,7), antinodes)


if __name__ == '__main__':
    unittest.main(verbosity=2)

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_coords(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1,1
33,2
11,5
12,3
3,8
""")

    coords = puzzle.coords
    self.assertEqual(len(coords), 5)

    self.assertIn((1,1), coords)
    self.assertIn((33,2), coords)
    self.assertIn((11,5), coords)
    self.assertIn((12,3), coords)
    self.assertIn((3,8), coords)

  def test_puzzle_finds_largest_rectangle(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1,1
33,2
11,5
12,3
3,8
""")

    size, corners = puzzle.find_largest_rectangle()

    self.assertEqual(217, size)
    self.assertIn((33,2), corners)
    self.assertIn((3,8), corners)

  def test_puzzle_fills_green_tiles(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1,1
33,1
33,5
11,5
11,3
8,3
1,3
""")

    puzzle.fill_green_tiles()
    
    puzzle.print_debug()

if __name__ == '__main__':
    unittest.main(verbosity=2)

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_grids(self):
    puzzle = puz.Puzzle()
    puzzle.process("""..
##

#.#
###
...

""")
    self.assertEqual(len(puzzle.grids), 2)
    self.assertEqual(puzzle.grids[1].width, 3)
    self.assertEqual(puzzle.grids[1].height, 3)

  def test_grid_finds_horizontal_reflectiion(self):
    grid = puz.Puzzle.Grid("""##.
###
##.""")
    
    self.assertEqual(grid.hreflect(), (1,2))

  def test_grid_no_horizontal_is_none(self):
    grid = puz.Puzzle.Grid("""#.#
###
##.""")
    
    self.assertEqual(grid.hreflect(), None)

  def test_grid_finds_vertical_reflectiion(self):
    grid = puz.Puzzle.Grid("""##.
###
.#.
.#.
###""")
    
    self.assertEqual(grid.vreflect(), (3,4))

  def test_grid_no_vertical_is_none(self):
    grid = puz.Puzzle.Grid("""#.#
###
##.""")
    
    self.assertEqual(grid.vreflect(), None)

  def test_grid_smudge_hreflect_non_for_true_reflect(self):
    grid = puz.Puzzle.Grid("""##.
###
##.""")
    
    self.assertEqual(grid.smudge_hreflect(), None)

  def test_grid_smudge_hreflects_when_off_by_1_cell(self):
    grid = puz.Puzzle.Grid("""###
###
##.""")
    
    self.assertEqual(grid.smudge_hreflect(), (2,3))

  def test_grid_smudge_vreflect_non_for_true_reflect(self):
    grid = puz.Puzzle.Grid("""#..
###
###""")
    
    self.assertEqual(grid.smudge_vreflect(), None)

  def test_grid_smudge_hreflects_when_off_by_1_cell(self):
    grid = puz.Puzzle.Grid("""#..
###
.##""")
    
    self.assertEqual(grid.smudge_vreflect(), (2,3))

if __name__ == '__main__':
    unittest.main()

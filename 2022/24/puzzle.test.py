import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_locates_start_and_end(self):
    puzzle = puz.Puzzle()
    puzzle.process("""#.######
#......#
#......#
######.#
""")
    
    self.assertEquals(puzzle.start, (1,0))
    self.assertEquals(puzzle.end, (6,3))

  def test_puzzle_locates_blizards(self):
    puzzle = puz.Puzzle()
    puzzle.process("""#.######
#>.....#
#...^..#
######.#
""")
    
    self.assertEquals(puzzle.blizard_at((1,1)), True)
    self.assertEquals(puzzle.blizard_at((1,2)), False)
    self.assertEquals(puzzle.blizard_at((4,2)), True)
    self.assertEquals(puzzle.blizard_at((5,2)), False)

  def test_puzzle_blizards_move_with_time(self):
    #Q: How does up/dn work with entrance/exit?
    # Map does not have such wind
    puzzle = puz.Puzzle()
    puzzle.process("""#.######
#>....<#
#.v.^..#
#......#
######.#
""")
    
    self.assertEquals(puzzle.blizard_at((1,1),2), False)
    self.assertEquals(puzzle.blizard_at((3,1),2), True)
    self.assertEquals(puzzle.blizard_at((4,1),2), True)
    self.assertEquals(puzzle.blizard_at((2,1),2), True)
    self.assertEquals(puzzle.blizard_at((4,3),2), True)

  def test_move_not_include_walls(self):
    puzzle = puz.Puzzle()
    puzzle.process("""#.######
#>....<#
#.v.^..#
#......#
######.#
""")

    options = puzzle.options(puzzle.start, 1)
    self.assertEquals((0,0) in options, False)
    self.assertEquals((2,0) in options, False)
    self.assertEquals((1,1) in options, True)

  def test_move_includes_exit(self):
    puzzle = puz.Puzzle()
    puzzle.process("""#.######
#>....<#
#.v.^..#
#......#
######.#
""")

    options = puzzle.options((6,3), 1)
    self.assertEquals((6,4) in options, True)

  def test_move_not_into_wind(self):
    puzzle = puz.Puzzle()
    puzzle.process("""#.######
#>....<#
#.v.^..#
#......#
######.#
""")

    options = puzzle.options((1,3), 0)
    self.assertEquals((2,3) in options, True)
    options = puzzle.options((1,3), 1)
    self.assertEquals((2,3) in options, False)


if __name__ == '__main__':
    unittest.main()

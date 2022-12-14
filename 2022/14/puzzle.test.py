import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_draws_map(self):
    puzzle = puz.Puzzle()
    puzzle.process("""400,4 -> 400,10 -> 410,10
430,8 -> 425,8 -> 425,5 -> 420,5    
""")

    self.assertEquals(puzzle.map_at(400,4), '#')
    self.assertEquals(puzzle.map_at(400,9), '#')
    self.assertEquals(puzzle.map_at(400,11), None)
    self.assertEquals(puzzle.map_at(409,10), '#')

    self.assertEquals(puzzle.map_at(421,5), '#')
    self.assertEquals(puzzle.map_at(426,5), None)
    self.assertEquals(puzzle.map_at(425,8), '#')
    self.assertEquals(puzzle.map_at(426,8), '#')
    self.assertEquals(puzzle.map_at(430,8), '#')

  def test_sand_lands_on_rock(self):
    puzzle = puz.Puzzle()
    puzzle.process("""498,5 -> 502,5
""")

    puzzle.drop_sand()
    self.assertEquals(puzzle.map_at(500,4), 'o')

  def test_sand_falls_left(self):
    puzzle = puz.Puzzle()
    puzzle.process("""498,5 -> 502,5
""")

    puzzle.drop_sand()
    puzzle.drop_sand()
    self.assertEquals(puzzle.map_at(499,4), 'o')

  def test_sand_falls_right(self):
    puzzle = puz.Puzzle()
    puzzle.process("""498,5 -> 502,5
""")

    puzzle.drop_sand()
    puzzle.drop_sand()
    puzzle.drop_sand()
    self.assertEquals(puzzle.map_at(501,4), 'o')

  def test_sand_that_does_not_land_returns_false(self):
    puzzle = puz.Puzzle()
    puzzle.process("""501,5 -> 502,5
""")

    lands = puzzle.drop_sand()
    self.assertEquals(lands, False)

if __name__ == '__main__':
    unittest.main()

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_shape_moves_with_wind(self):
    puzzle = puz.Puzzle()
    puzzle.process(""">><<<>><><><""")

    puzzle.tick() #Rock 1 falling

    self.assertEquals(puzzle.falling, 0)
    self.assertEquals(puzzle.pos, (3,2))

  def test_puzzle_shape_does_not_blow_past_right(self):
    puzzle = puz.Puzzle()
    puzzle.process(""">><<<>><><><""")

    puzzle.tick() #Rock 1 falling
    puzzle.tick() #Rock 1 falling

    self.assertEquals(puzzle.falling, 0)
    self.assertEquals(puzzle.pos, (3,1))

  def test_puzzle_shape_does_not_blow_past_left(self):
    puzzle = puz.Puzzle()
    puzzle.process("""<<<>><><><""")

    puzzle.tick() #Rock 1 falling
    puzzle.tick() 
    puzzle.tick() 

    self.assertEquals(puzzle.falling, 0)
    self.assertEquals(puzzle.pos, (0,0))

  def test_puzzle_shape_lands_when_cannot_fall(self):
    puzzle = puz.Puzzle()
    puzzle.process("""<<<<>><><><""")

    puzzle.tick() #Rock 1 falling
    puzzle.tick() 
    puzzle.tick() 
    puzzle.tick() 

    self.assertEquals(puzzle.rock_at(0,0), True)
    self.assertEquals(puzzle.rock_at(1,0), True)
    self.assertEquals(puzzle.rock_at(2,0), True)
    self.assertEquals(puzzle.rock_at(3,0), True)
    self.assertEquals(puzzle.rock_at(4,0), False)
    self.assertEquals(puzzle.rock_at(0,1), False)

    #New Rock
    self.assertEquals(puzzle.falling, 1)
    self.assertEquals(puzzle.pos, (2,4))

  def test_puzzle_shape_lands_on_shapes(self):
    puzzle = puz.Puzzle()
    puzzle.process("""<<<<><><><><>""")

    puzzle.tick() #Rock 1 falling
    puzzle.tick() 
    puzzle.tick() 
    puzzle.tick() 
    puzzle.tick() #Rock 2 falling
    puzzle.tick() 
    puzzle.tick() 
    puzzle.tick() 
    puzzle.tick() 

    self.assertEquals(puzzle.rock_at(2,1), False)
    self.assertEquals(puzzle.rock_at(3,1), True)
    self.assertEquals(puzzle.rock_at(4,1), False)
    self.assertEquals(puzzle.rock_at(3,2), True)
    self.assertEquals(puzzle.rock_at(3,3), True)


if __name__ == '__main__':
    unittest.main()

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_map(self):
    puzzle = puz.Puzzle()
    puzzle.process("""   ..#   
   .#..  
.......  
..#....  
     ....
     .#..

1R1L1L1L1L
""")

    
    self.assertEquals(puzzle.tile_at(0,0), None)
    self.assertEquals(puzzle.tile_at(3,0), '.')
    self.assertEquals(puzzle.tile_at(5,0), '#')

    self.assertEquals(puzzle.tile_at(5,5), '.')
    self.assertEquals(puzzle.tile_at(6,5), '#')
    self.assertEquals(puzzle.tile_at(4,5), None)

  def test_puzzle_neighbours_in_map(self):
    puzzle = puz.Puzzle()
    puzzle.process("""   ..#   
   .#..  
.......  
..#....  
     ....
     .#..

1R1L1L1L1L
""")

    self.assertEquals(puzzle.left(4,2), (3,2))
    self.assertEquals(puzzle.right(4,2), (5,2))
    self.assertEquals(puzzle.up(4,2), (4,1))
    self.assertEquals(puzzle.down(4,2), (4,3))


  def test_puzzle_neighbours_loop_up_and_right(self):
    puzzle = puz.Puzzle()
    puzzle.process("""   ..#   
   .#..  
.......  
..#....  
     ....
     .#..
     ....

1R1L1L1L1L
""")
    self.assertEquals(puzzle.left(8,4), (7,4))
    self.assertEquals(puzzle.right(8,4), (5,4))
    self.assertEquals(puzzle.up(8,4), (8,6))
    self.assertEquals(puzzle.down(8,4), (8,5))

  def test_puzzle_neighbours_loop_down_and_left(self):
    puzzle = puz.Puzzle()
    puzzle.process("""   ..#  
   .#..  
.......  
..#....  
     ....
     .#..
     ....

1R1L1L1L1L
""")
    self.assertEquals(puzzle.left(5,6), (8,6))
    self.assertEquals(puzzle.right(5,6), (6,6))
    self.assertEquals(puzzle.up(5,6), (5,5))
    self.assertEquals(puzzle.down(5,6), (5,0))

  def test_puzzle_start_position(self):
    puzzle = puz.Puzzle()
    puzzle.process("""   ..#  
   .#..  
.......  
..#....  
     ....
     .#..
     ....

1R1L1L1L1L
""")
    self.assertEquals(puzzle.start, ((3,0), '>'))

  def test_puzzle_moves(self):
    puzzle = puz.Puzzle()
    puzzle.process("""   ..#   
   .#..  
.......  
..#....  
     ....
     .#..
     ....

10R10R1L10L3L
""")
    loc, bear, _ = puzzle.move()
    self.assertEquals(loc, (6,2))
    self.assertEquals(bear, '^')

if __name__ == '__main__':
    unittest.main()

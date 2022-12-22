import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_map(self):
    puzzle = puz.Puzzle()
    puzzle.process("""      .11
      111   
      111   
222333444   
222333444   
222333444   
      555666
      555666
      555666

1R1L1L1L1L
""")
    
    self.assertEquals(puzzle.tile_at(0,0), None)
    self.assertEquals(puzzle.tile_at(6,0), '.')
    self.assertEquals(puzzle.tile_at(7,0), '1')

    self.assertEquals(puzzle.tile_at(5,5), '3')
    self.assertEquals(puzzle.tile_at(6,5), '4')
    self.assertEquals(puzzle.tile_at(4,7), None)

  def test_puzzle_neighbours_in_map(self):
    puzzle = puz.Puzzle()
    puzzle.process("""      .11
      111   
      111   
222333444   
222333444   
222333444   
      555666
      555666
      555666

1R1L1L1L1L
""")

    self.assertEquals(puzzle.left(4,2),  ((3,2), '<'))
    self.assertEquals(puzzle.right(4,2), ((5,2), '>'))
    self.assertEquals(puzzle.up(4,2),    ((4,1), '^'))
    self.assertEquals(puzzle.down(4,2),  ((4,3), 'v'))


  def test_puzzle_up_face1_goes2_face_down(self):
    puzzle = puz.Puzzle()
    puzzle.process("""        .111
        1111
        1111
        1111
222233334444
222233334444
222233334444
222233334444
        55556666
        55556666
        55556666
        55556666

1R1L1L1L1L
""")
    self.assertEquals(puzzle.up(8,0), ((3,4), 'v'))
    self.assertEquals(puzzle.up(3,4), ((8,0), 'v'))

  def test_puzzle_up_face1_goes3_face_left(self):
    puzzle = puz.Puzzle()
    puzzle.process("""        .111
        1111
        1111
        1111
222233334444
222233334444
222233334444
222233334444
        55556666
        55556666
        55556666
        55556666

1R1L1L1L1L
""")
    self.assertEquals(puzzle.left(8,0), ((4,4), 'v'))
    self.assertEquals(puzzle.up(5,4), ((8,1), '>'))

  def test_puzzle_up_face1_goes6_face_right(self):
    puzzle = puz.Puzzle()
    puzzle.process("""        .111
        1111
        1111
        1111
222233334444
222233334444
222233334444
222233334444
        55556666
        55556666
        55556666
        55556666

1R1L1L1L1L
""")
    self.assertEquals(puzzle.right(11,0), ((15,11), '<'))
    self.assertEquals(puzzle.right(15,10), ((11,1), '<'))

  def test_puzzle_face2_goes6_face_left(self):
    puzzle = puz.Puzzle()
    puzzle.process("""        .111
        1111
        1111
        1111
222233334444
222233334444
222233334444
222233334444
        55556666
        55556666
        55556666
        55556666

1R1L1L1L1L
""")
    self.assertEquals(puzzle.left(0,5), ((14,11), '^'))
    self.assertEquals(puzzle.down(12,11), ((0,7), '>'))


  def test_puzzle_face2_goes5_face_down(self):
    puzzle = puz.Puzzle()
    puzzle.process("""        .111
        1111
        1111
        1111
222233334444
222233334444
222233334444
222233334444
        55556666
        55556666
        55556666
        55556666

1R1L1L1L1L
""")
    self.assertEquals(puzzle.down(0,7), ((11,11), '^'))
    self.assertEquals(puzzle.down(9,11), ((2,7), '^'))

  def test_puzzle_face3_goes5_face_down(self):
    puzzle = puz.Puzzle()
    puzzle.process("""        .111
        1111
        1111
        1111
222233334444
222233334444
222233334444
222233334444
        55556666
        55556666
        55556666
        55556666

1R1L1L1L1L
""")
    self.assertEquals(puzzle.down(4,7), ((8,11), '>'))
    self.assertEquals(puzzle.left(8,9), ((6,7), '^'))

  def test_puzzle_face4_goes6_face_right(self):
    puzzle = puz.Puzzle()
    puzzle.process("""        .111
        1111
        1111
        1111
222233334444
222233334444
222233334444
222233334444
        55556666
        55556666
        55556666
        55556666

1R1L1L1L1L
""")
    self.assertEquals(puzzle.right(11,4), ((15,8), 'v'))
    self.assertEquals(puzzle.up(12,8), ((11,7), '<'))

  def test_puzzle_netshape_differs(self):
    puzzle = puz.Puzzle()
    puzzle.process("""    .11166666
    11116666
    11116666
    11116666
    4444
    4444
    4444
    4444
33335555
33335555
33335555
33335555
2222
2222
2222
2222

1R1L1L1L1L
""")
    self.assertEquals(puzzle.up(4,0), ((0,12), '>'))
    self.assertEquals(puzzle.left(0,12), ((4,0), 'v'))

    self.assertEquals(puzzle.left(4,0), ((0,11), '>'))
    self.assertEquals(puzzle.left(0,11), ((4,0), '>'))

    self.assertEquals(puzzle.right(3,12), ((4,11), '^'))
    self.assertEquals(puzzle.down(4,11), ((3,12), '<'))

    self.assertEquals(puzzle.down(3,15), ((11,0), 'v'))
    self.assertEquals(puzzle.up(11,0), ((3,15), '^'))

    self.assertEquals(puzzle.left(4,4), ((0,8), 'v'))
    self.assertEquals(puzzle.up(0,8), ((4,4), '>'))

    self.assertEquals(puzzle.right(7,4), ((8,3), '^'))
    self.assertEquals(puzzle.down(8,3), ((7,4), '<'))

    self.assertEquals(puzzle.right(7,8), ((11,3), '<'))
    self.assertEquals(puzzle.right(11,3), ((7,8), '<'))

  def test_puzzle_start_position(self):
    puzzle = puz.Puzzle()
    puzzle.process("""      .11   
      111   
      111   
222333444   
222333444   
222333444   
      555666
      555666
      555666

1R1L1L1L1L
""")
    self.assertEquals(puzzle.start, ((6,0), '>'))

  def test_puzzle_moves(self):
    return
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

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_head_moves_up(self):
    puzzle = puz.Puzzle()
    puzzle.process("""U 5
""")
    
    self.assertEquals(puzzle.head, (0,5))

  def test_puzzle_head_moves_down(self):
    puzzle = puz.Puzzle()
    puzzle.process("""D 5
""")
    
    self.assertEquals(puzzle.head, (0,-5))

  def test_puzzle_head_moves_left(self):
    puzzle = puz.Puzzle()
    puzzle.process("""L 3
""")
    
    self.assertEquals(puzzle.head, (-3,0))

  def test_puzzle_head_moves_right(self):
    puzzle = puz.Puzzle()
    puzzle.process("""R 7
""")
    
    self.assertEquals(puzzle.head, (7,0))

  def test_puzzle_tail_does_not_move_when_not_pulled(self):
    puzzle = puz.Puzzle()
    puzzle.process("""R 1
""")
    
    self.assertEquals(puzzle.tails[0], (0,0))

  def test_puzzle_tail_pulls_right(self):
    puzzle = puz.Puzzle()
    puzzle.process("""R 2
""")
    
    self.assertEquals(puzzle.tails[0], (1,0))

  def test_puzzle_tail_pulls_left(self):
    puzzle = puz.Puzzle()
    puzzle.process("""L 2
""")
    
    self.assertEquals(puzzle.tails[0], (-1,0))

  def test_puzzle_tail_pulls_up(self):
    puzzle = puz.Puzzle()
    puzzle.process("""U 2
""")
    
    self.assertEquals(puzzle.tails[0], (0,1))

  def test_puzzle_tail_pulls_down(self):
    puzzle = puz.Puzzle()
    puzzle.process("""D 2
""")
    
    self.assertEquals(puzzle.tails[0], (0,-1))

  def test_puzzle_tail_pulls_north_east(self):
    puzzle = puz.Puzzle()
    puzzle.process("""R 1
U 2
""")
    
    self.assertEquals(puzzle.tails[0], (1,1))

  def test_puzzle_tail_pulls_north_west(self):
    puzzle = puz.Puzzle()
    puzzle.process("""L 1
U 2
""")
    
    self.assertEquals(puzzle.tails[0], (-1,1))

  def test_puzzle_tail_pulls_south_east(self):
    puzzle = puz.Puzzle()
    puzzle.process("""D 1
R 2
""")
    
    self.assertEquals(puzzle.tails[0], (1,-1))

  def test_puzzle_tail_pulls_south_west(self):
    puzzle = puz.Puzzle()
    puzzle.process("""D 1
L 2
""")
    
    self.assertEquals(puzzle.tails[0], (-1,-1))

  def test_puzzle_tail_pulls_throughout_move(self):
    puzzle = puz.Puzzle()
    puzzle.process("""R 1
U 4
""")
    
    self.assertEquals(puzzle.tails[0], (1,3))

  def test_puzzle_tail_pulls_chain(self):
    puzzle = puz.Puzzle()
    puzzle.process("""R 4
""")
    
    self.assertEquals(puzzle.tails[0], (3, 0))
    self.assertEquals(puzzle.tails[1], (2, 0))
    self.assertEquals(puzzle.tails[2], (1, 0))
    self.assertEquals(puzzle.tails[3], (0, 0))

if __name__ == '__main__':
    unittest.main()

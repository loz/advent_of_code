import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_finds_starting_position(self):
    puzzle = puz.Puzzle()
    puzzle.process("""     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 
""")
    self.assertEqual(puzzle.loc, (5,0))

  def test_puzzle_travels_to_corner(self):
    puzzle = puz.Puzzle()
    puzzle.process("""     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 
""")
    puzzle.travel()
    self.assertEqual(puzzle.loc, (5,5))

  def test_puzzle_corner_changes_direction(self):
    puzzle = puz.Puzzle()
    puzzle.process("""     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 
""")
    puzzle.travel()
    self.assertEqual(puzzle.direction, (1,0))

  def test_puzzle_collects_letters(self):
    puzzle = puz.Puzzle()
    puzzle.process("""     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 
""")
    puzzle.travel()
    puzzle.travel()
    puzzle.travel()
    puzzle.travel()
    puzzle.travel()
    self.assertEqual(puzzle.letters, ['A', 'B', 'C'])

  def test_puzzle_counts_steps(self):
    puzzle = puz.Puzzle()
    puzzle.process("""     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 
""")
    while not puzzle.finished:
      puzzle.travel()
    self.assertEqual(puzzle.steps, 38)

if __name__ == '__main__':
    unittest.main()

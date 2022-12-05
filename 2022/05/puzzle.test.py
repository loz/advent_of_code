import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_reads_crate_start(self):
    puzzle = puz.Puzzle()
    puzzle.process("""[A]            
[B] [D]    
[C] [E] [F]
 1   2   3 
""")
    
    self.assertEquals(puzzle.stacks[0], ['C','B','A'])
    self.assertEquals(puzzle.stacks[1], ['E','D'])
    self.assertEquals(puzzle.stacks[2], ['F'])

  def test_puzzle_reads_move_commands(self):
    puzzle = puz.Puzzle()
    puzzle.process("""[A]            
[B] [D]    
[C] [E] [F]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
""")
    
    self.assertEquals(puzzle.moves[0], (1, 2, 1))
    self.assertEquals(puzzle.moves[1], (3, 1, 3))

  def test_puzzle_executes(self):
    puzzle = puz.Puzzle()
    puzzle.process("""[A]            
[B] [D]    
[C] [E] [F]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
""")
    puzzle.execute()
    self.assertEquals(puzzle.stacks[0], ['C','B','A', 'D'])
    self.assertEquals(puzzle.stacks[1], ['E'])
    self.assertEquals(puzzle.stacks[2], ['F'])

    puzzle.execute()
    self.assertEquals(puzzle.stacks[0], ['C'])
    self.assertEquals(puzzle.stacks[1], ['E'])
    self.assertEquals(puzzle.stacks[2], ['F', 'D', 'A', 'B'])

    self.assertEquals(puzzle.execute(), False)

  def test_puzzle_execute_9001(self):
    puzzle = puz.Puzzle()
    puzzle.process("""[A]            
[B] [D]    
[C] [E] [F]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
""")
    puzzle.execute_9001()
    self.assertEquals(puzzle.stacks[0], ['C','B','A', 'D'])
    self.assertEquals(puzzle.stacks[1], ['E'])
    self.assertEquals(puzzle.stacks[2], ['F'])

    puzzle.execute_9001()
    self.assertEquals(puzzle.stacks[0], ['C'])
    self.assertEquals(puzzle.stacks[1], ['E'])
    self.assertEquals(puzzle.stacks[2], ['F', 'B', 'A', 'D'])

    self.assertEquals(puzzle.execute(), False)

if __name__ == '__main__':
    unittest.main()

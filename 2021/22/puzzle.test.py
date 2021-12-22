import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_turns_on(self):
    puzzle = puz.Puzzle()
    puzzle.process("""on x=2..3,y=0..1,z=2..2
""")
    self.assertTrue((2,0,2) in puzzle.on)
    self.assertTrue((3,1,2) in puzzle.on)

  def test_puzzle_turns_on(self):
    puzzle = puz.Puzzle()
    puzzle.process("""on x=0..4,y=0..4,z=0..4
off x=2..3,y=0..1,z=2..2
""")
    self.assertFalse((2,0,2) in puzzle.on)
    self.assertFalse((3,1,2) in puzzle.on)

if __name__ == '__main__':
    unittest.main()

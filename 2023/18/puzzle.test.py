import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_draws_Right(self):
    puzzle = puz.Puzzle()
    puzzle.process("""R 5 (#123123)
D 8 (#aaabbb)
L 5 (#abcefg)
U 3 (#aabbcc)
""")
    
    puzzle.dig1()
    self.assertEqual(puzzle.at(0,0), ('.', '.'))
    self.assertEqual(puzzle.at(4,0), ('.', '.'))
    self.assertEqual(puzzle.at(5,0), ('R', '#123123'))

  def test_puzzle_draws_Down(self):
    puzzle = puz.Puzzle()
    puzzle.process("""R 5 (#123123)
D 8 (#aaabbb)
L 5 (#abcefg)
U 3 (#aabbcc)
""")
    
    puzzle.dig1()
    self.assertEqual(puzzle.at(5,7), ('.', '.'))
    self.assertEqual(puzzle.at(5,8), ('D', '#aaabbb'))

  def test_puzzle_draws_Left(self):
    puzzle = puz.Puzzle()
    puzzle.process("""R 5 (#123123)
D 8 (#aaabbb)
L 5 (#abcefg)
U 3 (#aabbcc)
""")
    
    puzzle.dig1()
    self.assertEqual(puzzle.at(1,8), ('.', '.'))
    self.assertEqual(puzzle.at(0,8), ('L', '#abcefg'))

  def test_puzzle_draws_Up(self):
    puzzle = puz.Puzzle()
    puzzle.process("""R 5 (#123123)
D 8 (#aaabbb)
L 5 (#abcefg)
U 3 (#aabbcc)
""")
    
    puzzle.dig1()
    self.assertEqual(puzzle.at(0,6), ('.', '.'))
    self.assertEqual(puzzle.at(0,5), ('U', '#aabbcc'))

if __name__ == '__main__':
    unittest.main()

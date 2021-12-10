import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_spins(self):
    puzzle = puz.Puzzle()
    puzzle.process("""s1,s2
""")
    self.assertEqual(puzzle.programs, 'nopabcdefghijklm')

  def test_puzzle_exchange(self):
    puzzle = puz.Puzzle()
    puzzle.process("""x0/8,x8/4

""")
    self.assertEqual(puzzle.programs, 'ibcdafghejklmnop')

  def test_puzzle_partner(self):
    puzzle = puz.Puzzle()
    puzzle.process("""pa/h,pc/n

""")
    self.assertEqual(puzzle.programs, 'hbndefgaijklmcop')

if __name__ == '__main__':
    unittest.main()

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_genline(self):
    puzzle = puz.Puzzle()
    newline = puzzle.genline("..^^.")
    self.assertEqual(newline, ".^^^^")

if __name__ == '__main__':
    unittest.main()

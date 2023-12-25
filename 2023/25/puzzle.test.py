import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_graph(self):
    puzzle = puz.Puzzle()
    puzzle.process("""abc: def ghi
ghi: jkl sdf
xyz: def
""")
  
    roots = puzzle.roots()

    self.assertEqual("abc" in roots, True)
    self.assertEqual("abc" in roots, True)
    self.assertEqual(len(roots), 2)

if __name__ == '__main__':
    unittest.main()

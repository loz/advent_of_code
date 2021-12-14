import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_expands_polymers(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ABC

AB -> X
BC -> Y
""")
    puzzle.expand()
    chain = puzzle.chain_string()
    self.assertEqual(chain, 'AXBYC')

  def test_puzzle_calcs_min_max(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ABABABCABABAAAC

AB -> X
BC -> Y
""")
    mmin, mmax = puzzle.min_max()
    self.assertEqual(mmin, ('C', 2))
    self.assertEqual(mmax, ('A', 8))

if __name__ == '__main__':
    unittest.main()

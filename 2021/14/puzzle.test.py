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

  def test_puzzle_tracks_pairs(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ABC

AB -> X
BC -> Y
""")
    self.assertEqual(puzzle.pairs['AB'], 1)
    self.assertEqual(puzzle.pairs['BC'], 1)

  def test_puzzle_expands_pairs(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ABC

AB -> X
BC -> Y
""")
    # -> AXBYC
    puzzle.expand_pairs()
    self.assertEqual(puzzle.pairs['AX'], 1)
    self.assertEqual(puzzle.pairs['XB'], 1)
    self.assertEqual(puzzle.pairs['BY'], 1)
    self.assertEqual(puzzle.pairs['YC'], 1)

  def test_puzzle_counts_freq_with_pairs(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ABC

AB -> X
BC -> Y
""")
    # -> AXBYC
    puzzle.expand_pairs()
    freqs = puzzle.pair_freqs()
    self.assertEqual(freqs['A'], 1)
    self.assertEqual(freqs['B'], 1)
    self.assertEqual(freqs['C'], 1)
    self.assertEqual(freqs['Y'], 1)
    self.assertEqual(freqs['X'], 1)


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

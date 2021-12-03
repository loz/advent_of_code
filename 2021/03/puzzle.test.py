import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_counts_most_common(self):
    puzzle = puz.Puzzle()
    puzzle.process("""010110
111111
000000
""")
    #most common = 010110
    self.assertEqual(puzzle.gamma, 0b010110)

  def test_puzzle_counts_least_common(self):
    puzzle = puz.Puzzle()
    puzzle.process("""010110
111111
000000
""")
    #most common = 010110
    self.assertEqual(puzzle.epsilon, 0b101001)


  def test_puzzle_narrows_bitsets(self):
    puzzle = puz.Puzzle()
    puzzle.process("""010110
111111
000000
""")
    bitsets = puzzle.narrow(0, '1')
    self.assertEqual(bitsets, [['1', '1', '1', '1', '1', '1']])

  def test_puzzle_computes_o2rating(self):
    puzzle = puz.Puzzle()
    puzzle.process("""010110
111100
100000
""")
    self.assertEqual(puzzle.o2rating, 0b111100)

  def test_puzzle_computes_co2rating(self):
    puzzle = puz.Puzzle()
    puzzle.process("""010110
111100
000011
100000
""")
    self.assertEqual(puzzle.co2rating, 0b000011)
    

if __name__ == '__main__':
    unittest.main()

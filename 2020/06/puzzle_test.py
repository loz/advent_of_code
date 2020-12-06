import unittest
import puzzle as puz

INPUT="""abc

a
b
c

ab
ac

a
a
a
a

b
"""

class TestPuzzle(unittest.TestCase):

  def test_process_groups(self):
    puzzle = puz.Puzzle()
    puzzle.process(INPUT)
    self.assertEqual(len(puzzle.groups), 5)

  def test_let_freq(self):
    puzzle = puz.Puzzle()
    group = ['ab', 'ac']
    freqs = puzzle.let_freq(group)
    self.assertEqual(freqs['a'], 2)
    self.assertEqual(freqs['b'], 1)
    self.assertEqual(freqs['c'], 1)

  def test_calcs_union(self):
    puzzle = puz.Puzzle()
    puzzle.process(INPUT)
    common = puzzle.common_answers
    self.assertEqual(common[0], 3)
    self.assertEqual(common[1], 0)
    self.assertEqual(common[2], 1)
    self.assertEqual(common[3], 1)
    self.assertEqual(common[4], 1)

if __name__ == '__main__':
    unittest.main()

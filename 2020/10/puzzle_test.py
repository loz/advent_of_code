import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_calcs_differences(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1
2
4
5
6
9
""")
    diffs = puzzle.differences()
    self.assertEqual(diffs, [1,1,2,1,1,3,3])

  def test_counts_permutations(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1
4
5
6
7
10
11
12
15
16
19
""")
    count = puzzle.count_permutations()
    self.assertEqual(count, 8)

if __name__ == '__main__':
    unittest.main()

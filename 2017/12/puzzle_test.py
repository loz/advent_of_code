import unittest
import puzzle as puz

EXAMPLE="""0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5
"""

class TestPuzzle(unittest.TestCase):

  def test_builds_graph(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)

    self.assertTrue(puzzle.links_to(0, 0))
    self.assertTrue(puzzle.links_to(3, 2))
    self.assertTrue(puzzle.links_to(0, 2))

  def test_build_groups(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)

    groups = puzzle.groups()
    groups.sort()
    self.assertEqual(groups[0], [0,2,3,4,5,6])
    self.assertEqual(groups[1], [1])
    

if __name__ == '__main__':
    unittest.main()

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_list_of_bytes(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1,3
3,4
5,7
""")

    
    self.assertIn((1,3), puzzle.bytes)
    self.assertIn((3,4), puzzle.bytes)
    self.assertIn((5,7), puzzle.bytes)

  def test_puzzle_path_navigates_fallen_bytes(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1,0
3,1
1,2
3,2
0,3
0,4
1,4
2,4
3,4
""")

    """
S#...
...#.
.#.#.
#....
####E
    """
    
    corruption = puzzle.fall_bytes(len(puzzle.bytes))
    width = 4
    height = 4
    path = puzzle.solve(width, height, corruption)

    self.assertEqual([(0,0), (0,1), (1, 1), (2,1), (2,2), (2,3), (3,3), (4,3), (4,4)], path)

if __name__ == '__main__':
    unittest.main(verbosity=2)

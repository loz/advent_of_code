import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_components(self):
    puzzle = puz.Puzzle()
    puzzle.process("""0/1
1/2
2/3
3/4
4/5
""")
    self.assertEquals(puzzle.components[0], (0,1))
    self.assertEquals(puzzle.components[1], (1,2))
    self.assertEquals(puzzle.components[2], (2,3))
    self.assertEquals(puzzle.components[3], (3,4))
    self.assertEquals(puzzle.components[4], (4,5))

  def test_puzzle_options_work_either_side(self):
    puzzle = puz.Puzzle()
    puzzle.process("""0/1
1/2
2/0
3/4
4/5
""")
    self.assertEquals(puzzle.options(0), [(0,1), (2,0)])

if __name__ == '__main__':
    unittest.main()

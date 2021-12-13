import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_folds_paper_y(self):
    puzzle = puz.Puzzle()
    # #...
    # ....
    # ...#
    puzzle.process("""0,0
3,2

fold along y=1
""")
    puzzle.fold()
    paper = puzzle.to_str()
    self.assertEqual(paper, """#..#
""")

  def test_puzzle_folds_paper_x(self):
    puzzle = puz.Puzzle()
    # #...
    # ....
    # ...#
    puzzle.process("""0,0
3,2

fold along x=2
""")
    puzzle.fold()
    paper = puzzle.to_str()
    self.assertEqual(paper, """#.
..
.#
""")

if __name__ == '__main__':
    unittest.main()

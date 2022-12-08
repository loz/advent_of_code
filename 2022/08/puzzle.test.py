import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_builds_map(self):
    puzzle = puz.Puzzle()
    puzzle.process("""123
456
789
""")
    self.assertEquals(puzzle.chart(0,0), 1)
    self.assertEquals(puzzle.chart(0,2), 7)
    self.assertEquals(puzzle.chart(2,0), 3)
    self.assertEquals(puzzle.chart(2,2), 9)

  def test_puzzle_edges_are_visible(self):
    puzzle = puz.Puzzle()
    puzzle.process("""999
909
999
""")
    self.assertEquals(puzzle.visible(0,0), True)
    self.assertEquals(puzzle.visible(0,2), True)
    self.assertEquals(puzzle.visible(2,0), True)
    self.assertEquals(puzzle.visible(2,2), True)

  def test_puzzle_higher_all_round_is_invisible(self):
    puzzle = puz.Puzzle()
    puzzle.process("""010
101
010
""")
    self.assertEquals(puzzle.visible(1,1), False)

  def test_puzzle_same_all_round_is_invisible(self):
    puzzle = puz.Puzzle()
    puzzle.process("""010
111
010
""")
    self.assertEquals(puzzle.visible(1,1), False)

  def test_puzzle_shorter_up_is_visible(self):
    puzzle = puz.Puzzle()
    puzzle.process("""010
323
030
""")
    self.assertEquals(puzzle.visible(1,1), True)

  def test_puzzle_shorter_down_is_visible(self):
    puzzle = puz.Puzzle()
    puzzle.process("""030
323
010
""")
    self.assertEquals(puzzle.visible(1,1), True)

  def test_puzzle_shorter_left_is_visible(self):
    puzzle = puz.Puzzle()
    puzzle.process("""030
123
030
""")
    self.assertEquals(puzzle.visible(1,1), True)

  def test_puzzle_shorter_right_is_visible(self):
    puzzle = puz.Puzzle()
    puzzle.process("""030
321
030
""")
    self.assertEquals(puzzle.visible(1,1), True)

  def test_puzzle_calculates_scenic_score(self):
    puzzle = puz.Puzzle()
    puzzle.process("""30373
25512
65332
33549
35390
""")
    self.assertEquals(puzzle.score(2,1), 4)

  def test_puzzle_calculates_scenic_score2(self):
    puzzle = puz.Puzzle()
    puzzle.process("""0008000
0002000
0005000
8259538
0005000
0003000
0008000
""")
    #3 in all dir
    self.assertEquals(puzzle.score(3,3), 3*3*3*3)

  def test_puzzle_calculates_scenic_score3(self):
    puzzle = puz.Puzzle()
    puzzle.process("""0008000
0007000
0005000
8958568
0001000
0002000
0003000
""")
    #3 * 2 * 3 * 3
    self.assertEquals(puzzle.score(3,3), 3 * 2 * 3 * 3)

  def test_puzzle_calculates_scenic_score4(self):
    puzzle = puz.Puzzle()
    puzzle.process("""000000000000000000000000000000000000000000000000000000
085257652577482877454566142635223501265056342151423503
000000000000000000000000000000000000000000000000000000
""")
    #1 up, left, down
    #085257652577482877454566142635223501265056342151423503
    # *YYYYYYYYYYYY
    self.assertEquals(puzzle.score(1,1), 1 * 1 * 1 * 12)

if __name__ == '__main__':
    unittest.main()

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_number_is_number(self):
    puzzle = puz.Puzzle()
    puzzle.process("""root: 10
""")
    self.assertEquals(puzzle.eval("root"), 10)

  def test_puzzle_monkey_add(self):
    puzzle = puz.Puzzle()
    puzzle.process("""root: aaaa + bbbb
aaaa: 1
bbbb: 12
""")
    self.assertEquals(puzzle.eval("root"), 13)

  def test_puzzle_monkey_sub(self):
    puzzle = puz.Puzzle()
    puzzle.process("""root: bbbb - aaaa
aaaa: 1
bbbb: 12
""")
    self.assertEquals(puzzle.eval("root"), 11)

  def test_puzzle_monkey_mul(self):
    puzzle = puz.Puzzle()
    puzzle.process("""root: bbbb * aaaa
aaaa: 2
bbbb: 12
""")
    self.assertEquals(puzzle.eval("root"), 24)

  def test_puzzle_monkey_div(self):
    puzzle = puz.Puzzle()
    puzzle.process("""root: bbbb / aaaa
aaaa: 2
bbbb: 12
""")
    self.assertEquals(puzzle.eval("root"), 6)

if __name__ == '__main__':
    unittest.main()

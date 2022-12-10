import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_addx_add_in_2_cycles(self):
    puzzle = puz.Puzzle()
    puzzle.process("""addx 2
addx -5
addx 1
""")

    puzzle.execute()
    puzzle.execute()
    puzzle.execute()

    self.assertEquals(puzzle.x, 1 + 2)

  def test_puzzle_noop_does_nothing_in_1_cycle(self):
    puzzle = puz.Puzzle()
    puzzle.process("""addx 2
noop
addx 1
""")

    puzzle.execute()
    puzzle.execute()
    puzzle.execute()
    puzzle.execute()
    puzzle.execute()

    self.assertEquals(puzzle.x, 1 + 2 + 1)

  def test_puzzle_loops_infinitely(self):
    puzzle = puz.Puzzle()
    puzzle.process("""addx 2
noop
""")

    puzzle.execute()
    puzzle.execute()
    puzzle.execute()
    puzzle.execute()
    puzzle.execute()

    self.assertEquals(puzzle.x, 1 + 2 + 2)

if __name__ == '__main__':
    unittest.main()

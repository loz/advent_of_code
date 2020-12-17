import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_example_cycle_1(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".#.
..#
###
""")
    print puzzle.slice(0)
    puzzle.tick()
    print puzzle.slice(-1)
    print puzzle.slice(0)
    print puzzle.slice(-1)
    self.assertEqual(puzzle.slice(-1), """...
#..
..#
.#.
""")
    self.assertEqual(puzzle.slice(0), """...
#.#
.##
.#.
""")
    self.assertEqual(puzzle.slice(1), """...
#..
..#
.#.
""")


if __name__ == '__main__':
    unittest.main()

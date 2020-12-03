import unittest
import puzzle as puz

INPUT = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""

class TestPuzzle(unittest.TestCase):

  def test_counts_trees_no_wrap(self):
    puzzle = puz.Puzzle()
    puzzle.process("""..#.
..#.
#...
.#..
#...
....
""")
    self.assertEqual(puzzle.count_trees(0,1), 2)

  def test_counts_trees_with_wrap(self):
    puzzle = puz.Puzzle()
    puzzle.process("""..#.
.##.
#.#.
.#..
#...
....
""")
    self.assertEqual(puzzle.count_trees(1,1), 3)

  def test_counts_example_correctly(self):
    puzzle = puz.Puzzle()
    puzzle.process(INPUT)
    self.assertEqual(puzzle.count_trees(3,1), 7)

if __name__ == '__main__':
    unittest.main()

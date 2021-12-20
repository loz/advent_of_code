import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_algorithm(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".#.##.##.#

.#.#
#.#.
.#.#
####
""")
    self.assertEqual(puzzle.algorithm, ['.', '#', '.', '#', '#', '.', '#', '#', '.', '#'])

  def test_puzzle_parses_map(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".#.##.##.#

.#.#
#.#.
.#.#
####
""")
    row = puzzle.map[2]
    self.assertEqual(row, ['.', '#', '.', '#'])
    self.assertEqual(puzzle.infinite,'.')

  def test_puzzle_retrieves_matrix(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".#.##.##.#

.#.#
#.#.
.#.#
####
""")
    matrix = puzzle.get_matrix(1,1)
    self.assertEqual(matrix, '.#.#.#.#.')

  def test_puzzle_retrieves_matrix_infinitely(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".#.##.##.#

.#.#
#.#.
.#.#
####
""")
    matrix = puzzle.get_matrix(0,0)
    self.assertEqual(matrix, '.....#.#.')

  def test_puzzle_retrieves_matrix_infinitely2(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".#.##.##.#

#..#.
#....
##..#
..#..
..###
""")
    matrix = puzzle.get_matrix(0,-1)
    self.assertEqual(matrix, '.......#.')

  def test_puzzle_calculates_enhance(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".#.##.##..?

.#.#
#.#.
.#.#
####
""")
    newpixel = puzzle.enhance(0,0)
    #  .....#.#. -> 1010 -> 10
    self.assertEqual(newpixel, '?')


if __name__ == '__main__':
    unittest.main()

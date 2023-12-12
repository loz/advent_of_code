import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_springs_and_checksums(self):
    puzzle = puz.Puzzle()
    puzzle.process("""#.#.### 1,1,3
.#...#....###. 1,1,3
""")
    self.assertEqual(puzzle.records[0], '#.#.###')
    self.assertEqual(puzzle.checks[0], [1,1,3])

  def test_puzzle_possible_combinations_no_unknown_is_one(self):
    puzzle = puz.Puzzle()
    puzzle.process("""#.#.### 1,1,3
.#...#....###. 1,1,3
""")
    
    self.assertEqual(puzzle.possible('#.#.###', [1,1,3]), 1)

  def test_puzzle_possible_with_one_option(self):
    puzzle = puz.Puzzle()
    puzzle.process("""#.#.### 1,1,3
.#...#....###. 1,1,3
""")
    
    self.assertEqual(puzzle.possible('#.#.???', [1,1,3]), 1)

  def test_puzzle_possible_with_two_option(self):
    puzzle = puz.Puzzle()
    puzzle.process("""#.#.### 1,1,3
.#...#....###. 1,1,3
""")
    
    self.assertEqual(puzzle.possible('#.#.???', [1,1,2]), 2)

  def test_puzzle_not_possible(self):
    puzzle = puz.Puzzle()
    puzzle.process("""#.#.### 1,1,3
.#...#....###. 1,1,3
""")
    
    self.assertEqual(puzzle.possible('?..###', [2,3]), 0)

if __name__ == '__main__':
    unittest.main()

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_finds_longest_path(self):
    puzzle = puz.Puzzle()
    puzzle.process("""#.#######
#...#...#
#.#.#.#.#
#.#...#.#
#.#####.#
#.......#
#######.#
""")
    
    longest = puzzle.longest()
    #puzzle.dump_path(longest)

    self.assertEqual(len(longest), 17)
    self.assertEqual((7,1) in longest, True)

  def test_puzzle_must_follow_down_slopes(self):
    puzzle = puz.Puzzle()
    puzzle.process("""#.#######
#v..#...#
#.#.#.#.#
#.#...#.#
#.#####.#
#.......#
#######.#
""")
    
    longest = puzzle.longest()
    #puzzle.dump_path(longest)

    self.assertEqual(len(longest), 13)
    self.assertEqual((1,2) in longest, True)

  def test_puzzle_must_follow_right_slopes(self):
    puzzle = puz.Puzzle()
    puzzle.process("""#.#######
#...#...#
#.#.#.#.#
#.#..>..#
#######.#
#.......#
#######.#
""")
    
    longest = puzzle.longest()
    #puzzle.dump_path(longest)

    self.assertEqual(len(longest), 13)

  def test_puzzle_must_follow_up_slopes(self):
    puzzle = puz.Puzzle()
    puzzle.process("""#.#######
#...#...#
#.#^#.#.#
#.#...#.#
#.#####.#
#.......#
#######.#
""")
    
    longest = puzzle.longest()
    #puzzle.dump_path(longest)

    self.assertEqual(len(longest), 13)

  def test_puzzle_must_follow_left_slopes(self):
    puzzle = puz.Puzzle()
    puzzle.process("""#.#######
#..<#...#
#.#.#.#.#
#.#...#.#
#.#####.#
#.......#
#######.#
""")
    
    longest = puzzle.longest()
    #puzzle.dump_path(longest)

    self.assertEqual(len(longest), 13)
if __name__ == '__main__':
    unittest.main()

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_locates_numbers_on_schematic(self):
    puzzle = puz.Puzzle()
    puzzle.process("""123...23
..*.....
..345..8
......+.
12..34..
.....445
""")
    self.assertEqual(puzzle.at(4,4), '34')

  def test_puzzle_not_part_ajacent_to_no_symbol(self):
    puzzle = puz.Puzzle()
    puzzle.process("""123...23
..*.....
..345..8
......+.
12..34..
.....445
""")
    self.assertEqual(puzzle.isPart(5,5), False)

  def test_puzzle_doesnot_have_part_with_bug(self):
    puzzle = puz.Puzzle()
    puzzle.process("""............830..743..
.......284.....*......
....%.........976..679
""")
    self.assertEqual(puzzle.isPart(17,0), False)

  def test_puzzle_is_part_ajacent_to_symbol(self):
    puzzle = puz.Puzzle()
    puzzle.process("""123...23
..*.....
..345..8
........
12&.34..
....@445
""")
    self.assertEqual(puzzle.isPart(2,2), True)
    self.assertEqual(puzzle.isPart(0,0), True)
    self.assertEqual(puzzle.isPart(0,4), True)
    self.assertEqual(puzzle.isPart(5,5), True)

  def test_puzzle_finds_stars(self):
    puzzle = puz.Puzzle()
    puzzle.process("""123...23
..*.....
..345..8
........
12*.34..
....*445
""")
    stars = puzzle.stars
    self.assertEqual((2,1) in stars, True)
    self.assertEqual((2,4) in stars, True)
    self.assertEqual((4,5) in stars, True)

if __name__ == '__main__':
    unittest.main()

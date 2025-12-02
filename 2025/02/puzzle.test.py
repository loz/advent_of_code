import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_ids(self):
    puzzle = puz.Puzzle()
    puzzle.process("""123,456,789
""")
    self.assertEqual(len(puzzle.ids), 3)
    self.assertEqual(puzzle.ids[0], '123')
    self.assertEqual(puzzle.ids[1], '456')
    self.assertEqual(puzzle.ids[2], '789')

  def test_puzzle_checks_range_for_invalids(self):
    puzzle = puz.Puzzle()
    puzzle.process("""123,456,789
""")

    invalid = puzzle.scan_invalid('1-25')
    self.assertEqual(len(invalid), 2)
    self.assertEqual(invalid[0], 11)
    self.assertEqual(invalid[1], 22)

  def test_puzzle_checks_range_for_invalids_of_any_sequence(self):
    puzzle = puz.Puzzle()
    puzzle.process("""123,456,789
""")

    invalid = puzzle.scan_invalid2('565653-565659')
    self.assertEqual(len(invalid), 1)
    self.assertEqual(invalid[0], 565656)

if __name__ == '__main__':
    unittest.main(verbosity=2)

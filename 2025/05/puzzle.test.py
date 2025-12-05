import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_ranges_and_ids(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1-3
2-6

1
5
12
""")

    self.assertEqual(len(puzzle.ranges), 2)
    self.assertEqual(len(puzzle.ids), 3)

    self.assertIn(range(1,4), puzzle.ranges)
    self.assertIn(5, puzzle.ids)

  def test_merging_ranges_when_new_start_overlaps(self):
    puzzle = puz.Puzzle()
    
    existing = [range(1,10)]
    merged = puzzle.merge_covered(existing, range(5,12))

    self.assertEqual(len(merged), 1)
    self.assertIn(range(1,12), merged)

  def test_merging_ranges_when_new_end_overlaps(self):
    puzzle = puz.Puzzle()
    
    existing = [range(1,10), range(15,20)]
    merged = puzzle.merge_covered(existing, range(12,16))

    self.assertEqual(len(merged), 2)
    self.assertIn(range(12,20), merged)

  def test_merging_ranges_when_new_fully_in_existing(self):
    puzzle = puz.Puzzle()
    
    existing = [range(1,10), range(15,20)]
    merged = puzzle.merge_covered(existing, range(16,18))

    self.assertEqual(len(merged), 2)
    self.assertIn(range(1,10), merged)
    self.assertIn(range(15,20), merged)

  def test_merging_ranges_when_a_existing_fully_in_new(self):
    puzzle = puz.Puzzle()
    
    existing = [range(1,10), range(16,18)]
    merged = puzzle.merge_covered(existing, range(15,20))

    self.assertEqual(len(merged), 2)
    self.assertIn(range(1,10), merged)
    self.assertIn(range(15,20), merged)

  def test_merge_joins_two_existing(self):
    puzzle = puz.Puzzle()
    
    existing = [range(3, 6), range(10, 15), range(16, 21)]
    merged = puzzle.merge_covered(existing, range(12,19))

    self.assertEqual(len(merged), 2)
    self.assertIn(range(3,6), merged)
    self.assertIn(range(10,21), merged)

if __name__ == '__main__':
    unittest.main(verbosity=2)

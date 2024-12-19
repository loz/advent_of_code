import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_towel_strips(self):
    puzzle = puz.Puzzle()
    puzzle.process("""a, ab, abc, b, d

aaa
bbb
ccc
""")

    self.assertEqual(len(puzzle.towels), 5)

    self.assertIn('a', puzzle.towels)
    self.assertIn('ab', puzzle.towels)
    self.assertIn('abc', puzzle.towels)
    self.assertIn('b', puzzle.towels)
    self.assertIn('d', puzzle.towels)

  def test_puzzle_parses_patterns(self):
    puzzle = puz.Puzzle()
    puzzle.process("""a, ab, abc, b, d

aaa
bbb
ccc
""")

    self.assertEqual(len(puzzle.patterns), 3)

    self.assertIn('aaa', puzzle.patterns)
    self.assertIn('bbb', puzzle.patterns)
    self.assertIn('ccc', puzzle.patterns)

  def test_puzzle_detects_valid_patterns(self):
    puzzle = puz.Puzzle()
    puzzle.process("""a, ab, abc, b, d

aaa
bbb
ccc
""")

    self.assertTrue(puzzle.valid_pattern('aaa'))
    self.assertTrue(puzzle.valid_pattern('bbb'))
    self.assertTrue(puzzle.valid_pattern('ababd'))
    self.assertTrue(puzzle.valid_pattern('ababc'))

  def test_puzzle_detects_invalid_patterns(self):
    puzzle = puz.Puzzle()
    puzzle.process("""a, ab, abc, b, d

aaa
bbb
ccc
""")

    self.assertFalse(puzzle.valid_pattern('ccc'))
    self.assertFalse(puzzle.valid_pattern('bcd'))
    self.assertFalse(puzzle.valid_pattern('edf'))

  def test_puzzle_counts_valid_combinations(self):
    puzzle = puz.Puzzle()
    puzzle.process("""a, ab, abc, b, d

aaa
bbb
ccc
""")

    self.assertEqual(puzzle.valid_combos('ccc'), 0)
    """
    a a b b
    a ab b
    """
    self.assertEqual(puzzle.valid_combos('aabb'), 2)

if __name__ == '__main__':
    unittest.main(verbosity=2)

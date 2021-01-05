import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_count_single_group(self):
    puzzle = puz.Puzzle()
    self.assertEqual(puzzle.count_group("{"), 0)
    self.assertEqual(puzzle.count_group("{}"), 1)

  def test_count_nested_group(self):
    puzzle = puz.Puzzle()
    self.assertEqual(puzzle.count_group("{{{}}}"), 3)
    self.assertEqual(puzzle.count_group("{{},{}}"), 3)
    self.assertEqual(puzzle.count_group("{{{},{},{{}}}}"), 6)

  def test_count_removes_garbage(self):
    puzzle = puz.Puzzle()
    self.assertEqual(puzzle.count_group("{<a>,<a>,<a>,<a>}"), 1)
    self.assertEqual(puzzle.count_group("{{<a>},{<a>},{<a>},{<a>}}"), 5)
    self.assertEqual(puzzle.count_group("{<{},{},{{}}>}"), 1)

  def test_count_handles_negated_chars(self):
    puzzle = puz.Puzzle()
    self.assertEqual(puzzle.count_group("{{<!>},{<!>},{<!>},{<a>}}"), 2)

  def test_score_groups(self):
    puzzle = puz.Puzzle()
    self.assertEqual(puzzle.score_group("{{{},{},{{}}}}"), 16)
    self.assertEqual(puzzle.score_group("{{<ab>},{<ab>},{<ab>},{<ab>}}"), 9)
    self.assertEqual(puzzle.score_group("{{<a!>},{<a!>},{<a!>},{<ab>}}"), 3)

  def test_count_garbage_chars(self):
    puzzle = puz.Puzzle()
    self.assertEqual(puzzle.count_garbage("<>"), 0)
    self.assertEqual(puzzle.count_garbage("<random characters>"), 17)
    self.assertEqual(puzzle.count_garbage("<<<<>"), 3)
    self.assertEqual(puzzle.count_garbage("<{!>}>"), 2)
    self.assertEqual(puzzle.count_garbage("<!!>"), 0)
    self.assertEqual(puzzle.count_garbage("<{o'i!a,<{i<a>"), 10)

if __name__ == '__main__':
    unittest.main()

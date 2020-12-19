import unittest
import puzzle as puz

EXAMPLE="""0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
"""

class TestPuzzle(unittest.TestCase):

  def test_parses_rules(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)

    self.assertEqual(puzzle.rules[0],[[4,1,5]])
    self.assertEqual(puzzle.rules[1],[[2,3],[3,2]])
    self.assertEqual(puzzle.rules[4],["a"])

  def test_parses_messages(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)

    self.assertEqual(puzzle.messages[0], 'ababbb')
    self.assertEqual(puzzle.messages[4], 'aaaabbb')
  
  def test_matches_rule(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)
  
    self.assertTrue(puzzle.matches(0, 'ababbb'))
    self.assertTrue(puzzle.matches(0, 'abbbab'))
    self.assertFalse(puzzle.matches(0, 'bababa'))

if __name__ == '__main__':
    unittest.main()

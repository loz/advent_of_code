import unittest
import puzzle as puz

INPUT = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc"""

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses(self):
    puzzle = puz.Puzzle()
    puzzle.process(INPUT)
    
    first = puzzle.passwords[0]
    rule, password = first
    self.assertEqual(rule, (1, 3, 'a'))
    self.assertEqual(password, 'abcde')

  def test_can_test_valid(self):
    puzzle = puz.Puzzle()
    good = ((1, 3, 'a'), 'a')
    bad =  ((2, 3, 'a'), 'a')
    
    self.assertTrue(puzzle.validPassword(good))
    self.assertFalse(puzzle.validPassword(bad))

  def test_can_test_valid2(self):
    puzzle = puz.Puzzle()
    good1 = ((1, 3, 'a'), 'abc')
    good2 = ((1, 3, 'a'), 'cba')
    bad1 = ((1, 3, 'a'), 'xbc')
    bad2 = ((1, 3, 'a'), 'aba')
    bad3 = ((1, 9, 'a'), 'aba')
    
    self.assertTrue(puzzle.validPassword2(good1))
    self.assertTrue(puzzle.validPassword2(good2))
    self.assertFalse(puzzle.validPassword2(bad1))
    self.assertFalse(puzzle.validPassword2(bad2))
    self.assertFalse(puzzle.validPassword2(bad3))

if __name__ == '__main__':
    unittest.main()

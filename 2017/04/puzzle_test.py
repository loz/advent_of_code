import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_valid_passphrase(self):
    puzzle = puz.Puzzle()
    self.assertTrue(puzzle.valid("aa bb cc dd"))
    self.assertTrue(puzzle.valid("aa cc dd"))
    self.assertTrue(puzzle.valid("aa bb aaa bbb"))

  def test_invalid_passphrase(self):
    puzzle = puz.Puzzle()
    self.assertFalse(puzzle.valid("aa bb cc aa"))
    self.assertFalse(puzzle.valid("aa cc cc"))
    self.assertFalse(puzzle.valid("aa bb aaa bb"))

  def test_invalid_anagrams_too(self):
    puzzle = puz.Puzzle()
    self.assertTrue(puzzle.valid("abcde fghij"))
    self.assertFalse(puzzle.valid("abcde xyz ecdab"))
    self.assertTrue(puzzle.valid("iiii oiii ooii oooi oooo"))
    self.assertFalse(puzzle.valid("oiii ioii iioi iiio"))

if __name__ == '__main__':
    unittest.main()

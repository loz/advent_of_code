import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_find_start_of_range(self):
    puzzle = puz.Puzzle()
    puzzle.process("abc")
    start = puzzle.find_start()
    index, char = start
    self.assertEqual(index, 18)
    self.assertEqual(char, '8')

  def test_puzzle_validate_is_key(self):
    puzzle = puz.Puzzle()
    puzzle.process("abc")
    self.assertFalse(puzzle.validKey(18, '8'))
    self.assertTrue(puzzle.validKey(39, 'e'))


if __name__ == '__main__':
    unittest.main()

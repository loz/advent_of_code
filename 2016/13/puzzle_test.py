import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_generates_open_spaces(self):
    puzzle = puz.Puzzle()
    puzzle.process(10)
    self.assertEqual(puzzle.generate(0,0), '.')
    self.assertEqual(puzzle.generate(5,3), '.')

  def test_generates_wall(self):
    puzzle = puz.Puzzle()
    puzzle.process(10)
    self.assertEqual(puzzle.generate(4,3), '#')
    self.assertEqual(puzzle.generate(1,0), '#')

if __name__ == '__main__':
    unittest.main()

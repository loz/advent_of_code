import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_walks_right(self):
    puzzle = puz.Puzzle()
    puzzle.process("""R

AAA = (BBB, CCC)
BBB = (ZZZ, ZZZ)
CCC = (AAA, BBB)
""")
  
    self.assertEqual(puzzle.start, 'AAA')
    self.assertEqual(puzzle.walk(), 'CCC')
    self.assertEqual(puzzle.walk(), 'BBB')
    self.assertEqual(puzzle.walk(), 'ZZZ')

  def test_puzzle_walks_left(self):
    puzzle = puz.Puzzle()
    puzzle.process("""L

AAA = (BBB, CCC)
BBB = (ZZZ, ZZZ)
CCC = (AAA, BBB)
""")
  
    self.assertEqual(puzzle.walk(), 'BBB')
    self.assertEqual(puzzle.walk(), 'ZZZ')

if __name__ == '__main__':
    unittest.main()

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_lines(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1234
5678
91011
""")
    batteries = puzzle.batteries
    self.assertEqual(len(batteries), 3)
    self.assertEqual(batteries[0], '1234')
    self.assertEqual(batteries[1], '5678')
    self.assertEqual(batteries[2], '91011')

  def test_puzzle_finds_largest_combination(self):
    puzzle = puz.Puzzle()
    joltage = puzzle.find_joltage('93457')
    self.assertEqual(joltage, 97)


  def test_puzzle_finds_largest_n_combination(self):
    puzzle = puz.Puzzle()
    joltage = puzzle.find_n_joltage('934758', 3)
    self.assertEqual(joltage, 978)
  
if __name__ == '__main__':
    unittest.main(verbosity=2)

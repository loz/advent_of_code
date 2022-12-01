import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_counts_calories(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1000
2000
""")
    self.assertEquals(puzzle.calories[0], 3000)

  def test_puzzle_counts_calories_for_each_elf(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1000
2000

3000
4000
""")
    self.assertEquals(puzzle.calories[1], 7000)
if __name__ == '__main__':
    unittest.main()

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_calculates_fuel_cost(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1,2,3,4
""")
    #1 + (1+2) + (1+2+3) + (1+2+3+4)
    self.assertEqual(puzzle.fuel_cost(0), 20)
    #0 + 1 + (1+2) + (1+2+3)
    self.assertEqual(puzzle.fuel_cost(1), 10)

  def test_puzzle_calculates_cheapest(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1,2,2,3,1,4,5
""")
    self.assertEqual(puzzle.cheapest(), (2, 12))

if __name__ == '__main__':
    unittest.main()

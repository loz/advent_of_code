import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_calculates_min_x_velocity(self):
    puzzle = puz.Puzzle()
    puzzle.define([20, 30], [-10, -5])
    x = puzzle.min_x
    self.assertEqual(x, 6)

  def test_puzzle_calculates_max_x_velocity(self):
    puzzle = puz.Puzzle()
    puzzle.define([20, 30], [-10, -5])
    x = puzzle.max_x
    self.assertEqual(x, 7)

  def test_puzzle_calculates_max_y_velocity(self):
    puzzle = puz.Puzzle()
    puzzle.define([20, 30], [-10, -5])
    y = puzzle.max_y
    self.assertEqual(y, 9)

  def test_puzzle_calculates_max_height(self):
    puzzle = puz.Puzzle()
    puzzle.define([20, 30], [-10, -5])
    y = puzzle.max_height
    self.assertEqual(y, 45)

  def test_puzzle_calculates_all_vectors(self):
    puzzle = puz.Puzzle()
    puzzle.define([20, 30], [-10, -5])
    puzzle.simulate()
    options = puzzle.options
    print options
    self.assertEqual(len(options), 112)

if __name__ == '__main__':
    unittest.main()

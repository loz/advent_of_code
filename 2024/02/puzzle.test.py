import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_lists(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1 2 3 4 5
10 8 7 6 5
""")
    self.assertEquals(puzzle.list(0), [1, 2, 3, 4, 5])
    self.assertEquals(puzzle.list(1), [10, 8, 7, 6, 5])

  def test_puzzle_safe_when_increasing(self):
    puzzle = puz.Puzzle()
    
    self.assertEquals(puzzle.safe([1, 2, 3, 4, 5]), True)

  def test_puzzle_safe_when_decreasing(self):
    puzzle = puz.Puzzle()
    
    self.assertEquals(puzzle.safe([10, 9, 8, 7, 6]), True)

  def test_puzzle_not_safe_when_increasing_by_less_than_1(self):
    puzzle = puz.Puzzle()
    
    self.assertEquals(puzzle.safe([1, 2, 2, 4, 5]), False)

  def test_puzzle_not_safe_when_increasing_by_more_than_3(self):
    puzzle = puz.Puzzle()
    
    self.assertEquals(puzzle.safe([1, 2, 3, 7, 8]), False)

  def test_puzzle_not_safe_when_decreasing_by_more_than_3(self):
    puzzle = puz.Puzzle()
    
    self.assertEquals(puzzle.safe([8, 7, 3, 2, 1]), False)

  def test_puzzle_not_safe_when_mixes_increase_and_decrease(self):
    puzzle = puz.Puzzle()
    
    self.assertEquals(puzzle.safe([1, 2, 3, 2, 1]), False)

  def test_puzzle_not_safe_when_bug_1(self):
    puzzle = puz.Puzzle()
    
    self.assertEquals(puzzle.safe([1, 3, 2, 4, 5]), False)

  def test_puzzle_tolerable_when_only_one_increasing_by_less_than_1(self):
    puzzle = puz.Puzzle()
    
    self.assertEquals(puzzle.tolerable([1, 2, 2, 4, 5]), True)

  def test_puzzle_not_tolerable_when_more_than_one_increasing_by_less_than_1(self):
    puzzle = puz.Puzzle()
    
    self.assertEquals(puzzle.tolerable([1, 2, 2, 4, 5]), True)
    self.assertEquals(puzzle.tolerable([1, 2, 2, 4, 4]), False)

  def test_puzzle_not_tolerable_when_more_than_one_increasing_by_more_than_3(self):
    puzzle = puz.Puzzle()
    
    self.assertEquals(puzzle.tolerable([1, 2, 3, 7, 5]), True)
    self.assertEquals(puzzle.tolerable([1, 2, 3, 7, 11]), False)

  def test_puzzle_not_tolerable_when_more_than_one_decreasing_by_more_than_3(self):
    puzzle = puz.Puzzle()
    
    self.assertEquals(puzzle.tolerable([4, 7, 3, 2, 1]), True)
    self.assertEquals(puzzle.tolerable([14, 7, 3, 2, 1]), False)

  def test_puzzle_not_tolerable_when_more_than_1_mixes_increase_and_decrease(self):
    puzzle = puz.Puzzle()
    
    self.assertEquals(puzzle.tolerable([1, 2, 3, 2, 1]), False)

  def test_puzzle_tolerable_when_bug2(self):
    puzzle = puz.Puzzle()
    
    self.assertEquals(puzzle.tolerable([16, 18, 20, 22, 23, 22]), True)

if __name__ == '__main__':
    unittest.main()

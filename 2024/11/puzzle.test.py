import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_lines_of_stones(self):
    puzzle = puz.Puzzle()
    puzzle.process("""0 1 2 3 4 5
""")
    self.assertEqual(puzzle.stones, [0, 1, 2, 3, 4, 5])

  def test_puzzle_blink_engraves_0_to_1(self):
    puzzle = puz.Puzzle()
    stones = [0]
    stones = puzzle.blink(stones)
    
    self.assertEqual(stones, [1])

  def test_puzzle_blink_splits_even_digits(self):
    puzzle = puz.Puzzle()
    stones = [1234]
    stones = puzzle.blink(stones)
    
    self.assertEqual(stones, [12, 34])

    stones = [1204]
    stones = puzzle.blink(stones)
    
    self.assertEqual(stones, [12, 4])

  def test_puzzle_blink_multiplies_by_2024_in_all_other_cases(self):
    puzzle = puz.Puzzle()
    stones = [123]
    stones = puzzle.blink(stones)
    
    self.assertEqual(stones, [123*2024])

  def test_puzzle_blink_n_counts_stones_in_generations(self):
    puzzle = puz.Puzzle()
    stones = [123]
    
    #123 -> 123*2024
    self.assertEqual(puzzle.blink_n(1, stones), 1)
    #248952 -> [248, 952] 
    self.assertEqual(puzzle.blink_n(2, stones), 2)
    #-> 248*2024, 952*2024
    self.assertEqual(puzzle.blink_n(3, stones), 2)
    #501,952, 1,926,848 -> [501, 952, 1,926,848*2024] 
    self.assertEqual(puzzle.blink_n(4, stones), 3)



if __name__ == '__main__':
    unittest.main(verbosity=2)

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_extracts_the_instructions(self):
    puzzle = puz.Puzzle()
    puzzle.process("""mul(1,2)""")
    self.assertEqual(puzzle.instructions[0], ('mul', 1, 2))

  def test_puzzle_extracts_multiple_instructions(self):
    puzzle = puz.Puzzle()
    puzzle.process("""mul(1,2)mul(3,4)""")
    self.assertEqual(puzzle.instructions[1], ('mul', 3,4))

  def test_puzzle_extracts_only_valid(self):
    puzzle = puz.Puzzle()
    puzzle.process("""mul(1,2mul(3,4)""")
    self.assertEqual(puzzle.instructions[0], ('mul', 3,4))

  def test_puzzle_extracts_do_instructions(self):
    puzzle = puz.Puzzle()
    puzzle.process("""mul(1,2)do()mul(3,4)""")
    self.assertEqual(puzzle.instructions[1], ('do', None, None))

  def test_puzzle_extracts_dont_instructions(self):
    puzzle = puz.Puzzle()
    puzzle.process("""mul(1,2)don't()mul(3,4)""")
    self.assertEqual(puzzle.instructions[1], ("don't", None, None))

if __name__ == '__main__':
    unittest.main()

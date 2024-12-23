import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_generates_next_secret(self):
    puzzle = puz.Puzzle()

    value = puzzle.generate(123)

    self.assertEqual(15887950, value)

  def test_generates_next_secret_n(self):
    puzzle = puz.Puzzle()

    value = puzzle.generate_n(123, 10)

    self.assertEqual(5908254, value)

  def test_counts_sequences(self):
    puzzle = puz.Puzzle()

    puzzle.count_sequences(123, 10)

    self.assertEqual( puzzle.sequence( (-3,  6, -1, -1) ), 4)
    self.assertEqual( puzzle.sequence( ( 6, -1, -1,  0) ), 4)
    self.assertEqual( puzzle.sequence( (-1, -1,  0,  2) ), 6)
    self.assertEqual( puzzle.sequence( (-1,  0,  2, -2) ), 4)
    self.assertEqual( puzzle.sequence( ( 0,  2, -2,  0) ), 4)
    self.assertEqual( puzzle.sequence( ( 2, -2,  0, -2) ), 2)

  def test_counts_only_first_occurence_in_a_single_count(self):
    puzzle = puz.Puzzle()

    puzzle.count_sequences(1, 2000)

    self.assertEqual( puzzle.sequence( (-3, 1, 0, 0) ), 7)


  def test_puzzle_parses_lines(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1
12
134
""")
    self.assertEqual(puzzle.numbers, [1, 12, 134])

if __name__ == '__main__':
    unittest.main(verbosity=2)

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_follows_combination_left(self):
    puzzle = puz.Puzzle()
    puzzle.process("""L15
""")
    self.assertEqual(puzzle.position, 50-15)

  def test_follows_combination_right(self):
    puzzle = puz.Puzzle()
    puzzle.process("""R34
""")
    self.assertEqual(puzzle.position, 50+34)

  def test_goes_around_clock(self):
    puzzle = puz.Puzzle()
    puzzle.process("""R51
""")
    self.assertEqual(puzzle.position, 1)

  def test_counts_zeros(self):
    puzzle = puz.Puzzle()
    puzzle.process("""R51
L1
R25
L30
R5
""")
    self.assertEqual(puzzle.position, 0)
    self.assertEqual(puzzle.zero_count, 2)

  def test_counts_zeros_with_protocol_0x434C49434B(self):
    puzzle = puz.Puzzle()
    puzzle.set0x434C49434B()

    puzzle.process("""R51
L1
R25
L30
R5
""")
    self.assertEqual(puzzle.position, 0)
    self.assertEqual(puzzle.zero_count, 4)

  def test_0x434C49434B_counts_multiple_rotations(self):
    puzzle = puz.Puzzle()
    puzzle.set0x434C49434B()

    puzzle.process("""R1000
""")
    self.assertEqual(puzzle.position, 50)
    self.assertEqual(puzzle.zero_count, 10)

if __name__ == '__main__':
    unittest.main(verbosity=2)

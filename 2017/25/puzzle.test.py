import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_tape_is_inifite(self):
    puzzle = puz.Puzzle()
    puzzle.left()
    puzzle.left()
    self.assertEquals(puzzle.read(), 0)
    puzzle.right()
    puzzle.right()
    puzzle.right()
    puzzle.right()
    self.assertEquals(puzzle.read(), 0)

  def test_puzzle_can_count_1s(self):
    puzzle = puz.Puzzle()
    puzzle.left()
    puzzle.left()
    puzzle.write(1)
    self.assertEquals(puzzle.read(), 1)
    puzzle.left()
    puzzle.right()
    puzzle.right()
    puzzle.right()
    puzzle.write(1)
    self.assertEquals(puzzle.read(), 1)
    puzzle.right()
    puzzle.right()
    self.assertEquals(puzzle.checksum(), 2)

  def test_puzzle_parses_state_machine(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Begin in state X.
Perform a diagnostic checksum after 123 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state Y.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state Z.
""")
    self.assertEqual(puzzle.start, 'X')
    self.assertEqual(puzzle.steps, 123)

    state = puzzle.states['A']
    self.assertEqual(state[0], (1, 'right', 'Y'))
    self.assertEqual(state[1], (0, 'left', 'Z'))

if __name__ == '__main__':
    unittest.main()

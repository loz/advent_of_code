import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_creates_broadcast_modules(self):
    puzzle = puz.Puzzle()
    puzzle.process("""broadcaster -> a, b
%a -> output
%b -> output
""")
    self.assertEqual(puzzle.broadcaster.type, 'button')

  def test_puzzle_creates_flip_flop_modules(self):
    puzzle = puz.Puzzle()
    puzzle.process("""broadcaster -> a, b
%a -> output
%b -> output
""")
    a = puzzle.lookup('a')
    self.assertEqual(a.type, 'flip-flop')
    b = puzzle.lookup('b')
    self.assertEqual(b.type, 'flip-flop')

  def test_puzzle_creates_conjunction(self):
    puzzle = puz.Puzzle()
    puzzle.process("""broadcaster -> a, b
&a -> output
&b -> output
""")
    a = puzzle.lookup('a')
    self.assertEqual(a.type, 'conjunction')
    b = puzzle.lookup('b')
    self.assertEqual(b.type, 'conjunction')

  def test_puzzle_wires_inputs_to_outputs(self):
    puzzle = puz.Puzzle()
    puzzle.process("""broadcaster -> a, b
%a -> output
%b -> output
""")
    bcast = puzzle.broadcaster
    a = puzzle.lookup('a')
    b = puzzle.lookup('b')

    self.assertEqual('a' in bcast.outputs, True)
    self.assertEqual('b' in bcast.outputs, True)

    self.assertEqual('broadcaster' in a.inputs, True)
    self.assertEqual('broadcaster' in b.inputs, True)

    self.assertEqual('output' in a.outputs, True)
    self.assertEqual('output' in b.outputs, True)

  def test_puzzle_button_pulses_low(self):
    puzzle = puz.Puzzle()
    puzzle.process("""broadcaster -> output
""")
    bcast = puzzle.broadcaster
    out = puzzle.output

    self.assertEqual(out.low_count, 0)
    bcast.pulse()
    self.assertEqual(out.low_count, 1)

  def test_puzzle_flip_flops_flip(self):
    puzzle = puz.Puzzle()
    puzzle.process("""broadcaster -> a
%a -> output
""")
    bcast = puzzle.broadcaster
    out = puzzle.output

    self.assertEqual(out.low_count, 0)
    bcast.pulse()
    bcast.pulse()
    bcast.pulse()
    self.assertEqual(out.high_count, 2)
    self.assertEqual(out.low_count, 1)

  def test_puzzle_conjunction_all_high_low_otherwise_high(self):
    puzzle = puz.Puzzle()
    puzzle.process("""broadcaster -> b, c
%b -> a
%c -> a
&a -> output
""")
    bcast = puzzle.broadcaster
    out = puzzle.output

    self.assertEqual(out.low_count, 0)
    bcast.pulse() #1->a (10a->1) 1->a (11a -> 0)
    self.assertEqual(out.high_count, 1)
    self.assertEqual(out.low_count, 1)
if __name__ == '__main__':
    unittest.main()

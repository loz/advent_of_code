import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_and_gate_sends_AND_of_input_to_output(self):
    source = puz.AndGate("source")
    dest = puz.AndGate("dest")

    #Wire Gates
    source.connect(dest)

    #No Signals sent
    self.assertEqual(dest.recieved, [])

    #Send Not AND
    source.send(0)
    self.assertEqual(dest.recieved, []) #Does not send until 2 inputs
    source.send(1)
    self.assertEqual(dest.recieved, [0])

    source.reset()
    dest.reset()

    #Send AND
    source.send(1)
    self.assertEqual(dest.recieved, [])
    source.send(1)
    self.assertEqual(dest.recieved, [1])

  def test_and_gate_sends_OR_of_input_to_output(self):
    source = puz.OrGate("source")
    dest = puz.OrGate("dest")

    #Wire Gates
    source.connect(dest)

    #Send 0
    source.send(0)
    source.send(0)
    self.assertEqual(dest.recieved, [0])

    source.reset()
    dest.reset()

    #Send 1
    source.send(1)
    source.send(0)
    self.assertEqual(dest.recieved, [1])

  def test_and_gate_sends_XOR_of_input_to_output(self):
    source = puz.XorGate("source")
    dest = puz.XorGate("dest")

    #Wire Gates
    source.connect(dest)

    #Send 0
    source.send(0)
    source.send(0)
    self.assertEqual(dest.recieved, [0])

    source.reset()
    dest.reset()

    #Send 0
    source.send(1)
    source.send(1)
    self.assertEqual(dest.recieved, [0])

    source.reset()
    dest.reset()
    
    #Send 1
    source.send(0)
    source.send(1)
    self.assertEqual(dest.recieved, [1])

  def test_puzzle_parses_initial_signals(self):
    puzzle = puz.Puzzle()
    puzzle.process("""one: 1
two: 0
three: 1

one AND two -> four
two OR three -> five
one XOR three -> six
""")

    self.assertEqual(puzzle.initial, {
      'one': 1, 'two': 0, 'three': 1
    })

  def test_puzzle_wires_gates(self):
    puzzle = puz.Puzzle()
    puzzle.process("""one: 1
two: 0
three: 1

one AND two -> four
two OR three -> five
one XOR three -> six
""")

    one = puzzle.wire('one')
    two = puzzle.wire('two')
    three = puzzle.wire('three')
    four = puzzle.wire('four')
    five = puzzle.wire('five')
    six = puzzle.wire('six')

    #1 & 2 => four
    self.assertEqual(four.state, None)
    one.send(0)
    two.send(1)
    self.assertEqual(four.state, 0)

    #two OR three => five
    self.assertEqual(five.state, None)
    three.send(0)
    self.assertEqual(five.state, 1)

    #one XOR three => six
    self.assertEqual(six.state, 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)

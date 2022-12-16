import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_options_have_move_to_room(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=123; tunnels lead to valves AA
""")
    curstate = puzzle.start
    options = puzzle.options(curstate)

    self.assertEquals(('DD', []) in options, True)
    self.assertEquals(('AA', ['AA']) in options, False)

  def test_puzzle_options_will_turn_on_if_flow_not_zero(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Valve AA has flow rate=10; tunnels lead to valves DD, II, BB
Valve BB has flow rate=123; tunnels lead to valves AA
""")
    curstate = puzzle.start
    options = puzzle.options(curstate)

    self.assertEquals(('AA', ['AA']) in options, True)

  def test_puzzle_options_will_not_turn_on_twice(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Valve AA has flow rate=10; tunnels lead to valves DD, II, BB
Valve BB has flow rate=123; tunnels lead to valves AA
""")
    curstate = puzzle.start
    curstate = ('AA', ['AA'])
    options = puzzle.options(curstate)

    self.assertEquals(('AA', ['AA']) in options, False)
    self.assertEquals(len(options), 3)

if __name__ == '__main__':
    unittest.main()

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_lines(self):
    puzzle = puz.Puzzle()
    puzzle.process("""[.#.] (1) (1,2) (2,3) {1,2,3}
[..##.] (1,4) (5) (2) (3) {5,4,6,3,3}
""")

    machines = puzzle.machines
    self.assertEqual(machines[0].diagram, '.#.')
    self.assertEqual(machines[0].buttons, [[1], [1,2], [2,3]])
    self.assertEqual(machines[0].joltages, [1,2,3])
    self.assertEqual(machines[1].diagram, '..##.')

  def test_machine_finds_shortest_press_path(self):
    machine = puz.Machine('[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}')

    shortest = machine.shortest_press()

    self.assertEqual(len(shortest), 2)

if __name__ == '__main__':
    unittest.main(verbosity=2)

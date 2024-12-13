import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_machines(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

""")

    self.assertEqual(len(puzzle.machines), 1)
    machine = puzzle.machines[0]

    self.assertEqual(machine.a, (94, 34))
    self.assertEqual(machine.b, (22, 67))
    self.assertEqual(machine.prize, (8400, 5400))

  def test_puzzle_calculates_min_cost_to_prize(self):
    machine = puz.Machine()
    machine.a = (10, 5)
    machine.b = (11, 22)
    machine.prize = (100, 50)

    cost = machine.calculate_min_cost()

    self.assertEqual(cost, (10, 0))

  def test_puzzle_calculates_no_cost_when_not_possible(self):
    machine = puz.Machine()
    machine.a = (10, 5)
    machine.b = (11, 22)
    machine.prize = (12, 6)

    cost = machine.calculate_min_cost()

    self.assertEqual(cost, None)

  def test_puzzle_calculates_uses_mix_of_a_b(self):
    machine = puz.Machine()
    machine.a = (10, 5)
    machine.b = (11, 22)
    machine.prize = (21, 27)

    cost = machine.calculate_min_cost()

    self.assertEqual(cost, (1, 1))

  def test_puzzle_calculates_uses_more_a_if_cheaper(self):
    machine = puz.Machine()
    machine.a = (50, 10)
    machine.b = (5, 1)
    machine.prize = (100, 20)

    cost = machine.calculate_min_cost()

    self.assertEqual(cost, (2, 0))

  def test_debug(self):
    machine = puz.Machine()
    #machine.a = (53, 64)
    #machine.b = (80, 21)
    #machine.prize = (7653, 6066) 
    machine.a = (3, 3)
    machine.b = (1, 1)
    machine.prize = (3*99, 3*99)
    machine.calculate_min_cost(True)

  def test_puzzle_calculates_uses_more_a_if_cheaper(self):
    machine = puz.Machine()
    machine.a = (50, 10)
    machine.b = (50, 10)
    machine.prize = (100, 20)

    cost = machine.calculate_min_cost()

    self.assertEqual(cost, (0, 2))

if __name__ == '__main__':
    unittest.main(verbosity=2)

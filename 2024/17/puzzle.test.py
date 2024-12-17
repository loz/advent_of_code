import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_program_state(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Register A: 123
Register B: 456
Register C: 789

Program: 1,2,3,4,5
""")

    machine = puzzle.machine
    self.assertEqual(machine.a, 123)
    self.assertEqual(machine.b, 456)
    self.assertEqual(machine.c, 789)
    self.assertEqual(machine.program, [1,2,3,4,5])


  def test_machine_adv_instruction_divides_int(self):
    machine = puz.Machine()
    machine.a = 5
    machine.program = [0, 1]

    machine.execute()

    self.assertEqual(machine.a, (5//2))

  def test_machine_adv_instruction_divides_int_with_combo(self):
    machine = puz.Machine()
    machine.a = 1234
    machine.b = 2
    machine.program = [0, 5]

    machine.execute()

    self.assertEqual(machine.a, (1234 // 4))

  def test_machine_bxl_instruction_bitwise_xors(self):
    machine = puz.Machine()
    machine.b = 5
    machine.program = [1, 3]

    machine.execute()

    self.assertEqual(machine.b, 5 ^ 3)

  def test_machine_bst_stores_modulo_8_in_b(self):
    machine = puz.Machine()
    machine.a = 15
    machine.program = [2, 4]

    machine.execute()

    self.assertEqual(machine.b, (15 % 8))

  def test_machine_jnz_does_nothing_when_a_is_zero(self):
    machine = puz.Machine()
    machine.a = 0
    machine.program = [3, 4, 1, 2, 3]

    machine.execute()

    self.assertEqual(machine.ip, 2)

  def test_machine_jnz_jumps_to_literal_if_a_non_zero(self):
    machine = puz.Machine()
    machine.a = 1
    machine.program = [3, 4, 1, 2, 3]

    machine.execute()

    self.assertEqual(machine.ip, 4)

  def test_machine_bxc_xors_b_and_c_into_b(self):
    machine = puz.Machine()
    machine.b = 12
    machine.c = 8
    machine.program = [4, 9]

    machine.execute()

    self.assertEqual(machine.b, 12 ^ 8)

  def test_machine_out_outputs_combo_modulo_8(self):
    machine = puz.Machine()
    machine.b = 12
    machine.program = [5, 5]

    machine.execute()

    self.assertEqual(machine.output, [12 % 8])

  def test_machine_bdv_instruction_divides_int_to_b(self):
    machine = puz.Machine()
    machine.a = 32
    machine.c = 2
    machine.program = [6, 6]

    machine.execute()

    self.assertEqual(machine.b, (32 // 4))

  def test_machine_cdv_instruction_divides_int_to_b(self):
    machine = puz.Machine()
    machine.a = 32
    machine.c = 3
    machine.program = [7, 6]

    machine.execute()

    self.assertEqual(machine.c, (32 // 8))

  def test_machine_halts(self):
    machine = puz.Machine()
    machine.a = 32
    machine.c = 3
    machine.program = [7, 6]

    self.assertEqual(machine.execute(), True)
    self.assertEqual(machine.execute(), False)

  def test_machine_examples(self):
    machine = puz.Machine()
    machine.c = 9
    machine.program = [2, 6]
    machine.execute()
    self.assertEqual(machine.b, 1)

    machine = puz.Machine()
    machine.a = 10
    machine.program = [5,0,5,1,5,4]
    while machine.execute():
      pass

    self.assertEqual(machine.output, [0, 1, 2])

    machine = puz.Machine()
    machine.a = 2024
    machine.program = [0,1,5,4,3,0]
    while machine.execute():
      pass

    self.assertEqual(machine.a, 0)
    self.assertEqual(machine.output, [4,2,5,6,7,7,7,7,3,1,0])

    machine = puz.Machine()
    machine.a = 2024
    machine.program = [0,1,5,4,3,0]
    while machine.execute():
      pass

if __name__ == '__main__':
    unittest.main(verbosity=2)

import unittest
import puzzle as puz

INPUT = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""

class TestPuzzle(unittest.TestCase):

  def test_nop(self):
    puzzle = puz.Puzzle()
    puzzle.process("""nop 0
""")
    puzzle.run_statement()
    self.assertEqual(puzzle.instruction_pointer, 1)

  def test_acc(self):
    puzzle = puz.Puzzle()
    puzzle.process("""acc -10
""")
    puzzle.run_statement()
    self.assertEqual(puzzle.accumulator, -10)

  def test_jmp(self):
    puzzle = puz.Puzzle()
    puzzle.process("""nop 0
jmp -1
""")
    puzzle.run_statement()
    puzzle.run_statement()
    self.assertEqual(puzzle.instruction_pointer, 0)

  def test_example(self):
    puzzle = puz.Puzzle()
    puzzle.process(INPUT)
    for i in range(1,7):
      puzzle.run_statement()
    self.assertEqual(puzzle.accumulator, 5)

if __name__ == '__main__':
    unittest.main()

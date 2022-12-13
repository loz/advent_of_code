import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_command_snd(self):
    puzzle = puz.Puzzle()
    puzzle.process("""snd 123
snd A
""")
    computer = puz.Puzzle.Computer(puzzle)

    computer.reg['A'] = 345
    computer.run()
    self.assertEqual(computer.sends, [123, 345])

  def test_puzzle_command_set(self):
    puzzle = puz.Puzzle()
    puzzle.process("""set A 123
set B 345
set C A
set E D
""")
    computer = puz.Puzzle.Computer(puzzle)
    computer.run()
    self.assertEqual(computer.reg['A'], 123)
    self.assertEqual(computer.reg['B'], 345)
    self.assertEqual(computer.reg['C'], 123)
    self.assertEqual(computer.reg['E'], 0)

  def test_puzzle_command_add(self):
    puzzle = puz.Puzzle()
    puzzle.process("""set A 123
set B 345
add B 100
add B A
""")
    computer = puz.Puzzle.Computer(puzzle)
    computer.run()
    self.assertEqual(computer.reg['B'], 345 + 100 + 123)

  def test_puzzle_command_sub(self):
    puzzle = puz.Puzzle()
    puzzle.process("""set A 123
set B 345
sub B 100
sub B A
""")
    computer = puz.Puzzle.Computer(puzzle)
    computer.run()
    self.assertEqual(computer.reg['B'], 345 - 100 - 123)

  def test_puzzle_command_mul(self):
    puzzle = puz.Puzzle()
    puzzle.process("""set A 123
set B 345
mul B 100
mul B A
""")
    computer = puz.Puzzle.Computer(puzzle)
    computer.run()
    self.assertEqual(computer.reg['B'], 345 * 100 * 123)

  def test_puzzle_command_mod(self):
    puzzle = puz.Puzzle()
    puzzle.process("""set A 123
set B 345
mod B 10
mod A B
""")
    computer = puz.Puzzle.Computer(puzzle)
    computer.run()
    self.assertEqual(computer.reg['B'], 5)
    self.assertEqual(computer.reg['A'], 3)

  def test_puzzle_command_rcv(self):
    puzzle = puz.Puzzle()
    puzzle.process("""snd 123
snd 345
set A 1
rcv A
set A 0
rcv A
set A 1
rcv A
rcv 1
rcv 0
""")
    computer = puz.Puzzle.Computer(puzzle)
    computer.run([123, 345, 456])
    self.assertEqual(computer.recieved, [123, 345, 456])

  def test_puzzle_command_jgz(self):
    puzzle = puz.Puzzle()
    puzzle.process("""snd 123
set A 0
jnz A 2
snd 345
set A 2
jnz A 2
snd 100
snd 200
set A -2
snd 300
add A 1
jnz A -2
""")
    computer = puz.Puzzle.Computer(puzzle)
    computer.run()
    self.assertEqual(computer.sends, [123, 345, 200, 300, 300])

  def test_puzzle_command_jnz(self):
    puzzle = puz.Puzzle()
    puzzle.process("""snd 123
set A 0
jgz A 2
snd 345
set A 2
jgz A 2
snd 100
snd 200
set A 2
snd 300
add A -1
jgz A -2
""")
    computer = puz.Puzzle.Computer(puzzle)
    computer.run()
    self.assertEqual(computer.sends, [123, 345, 200, 300, 300])

if __name__ == '__main__':
    unittest.main()

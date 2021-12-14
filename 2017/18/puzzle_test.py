import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_command_snd(self):
    puzzle = puz.Puzzle()
    puzzle.process("""snd 123
snd A
""")
    puzzle.reg['A'] = 345
    puzzle.run()
    self.assertEqual(puzzle.sounds, [123, 345])

  def test_puzzle_command_set(self):
    puzzle = puz.Puzzle()
    puzzle.process("""set A 123
set B 345
set C A
set E D
""")
    puzzle.run()
    self.assertEqual(puzzle.reg['A'], 123)
    self.assertEqual(puzzle.reg['B'], 345)
    self.assertEqual(puzzle.reg['C'], 123)
    self.assertEqual(puzzle.reg['E'], 0)

  def test_puzzle_command_add(self):
    puzzle = puz.Puzzle()
    puzzle.process("""set A 123
set B 345
add B 100
add B A
""")
    puzzle.run()
    self.assertEqual(puzzle.reg['B'], 345 + 100 + 123)

  def test_puzzle_command_mul(self):
    puzzle = puz.Puzzle()
    puzzle.process("""set A 123
set B 345
mul B 100
mul B A
""")
    puzzle.run()
    self.assertEqual(puzzle.reg['B'], 345 * 100 * 123)

  def test_puzzle_command_mod(self):
    puzzle = puz.Puzzle()
    puzzle.process("""set A 123
set B 345
mod B 10
mod A B
""")
    puzzle.run()
    self.assertEqual(puzzle.reg['B'], 5)
    self.assertEqual(puzzle.reg['A'], 3)

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
    puzzle.run()
    self.assertEqual(puzzle.recovered, [345, 345, 345])

  def test_puzzle_command_jgz(self):
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
    puzzle.run()
    self.assertEqual(puzzle.sounds, [123, 345, 200, 300, 300])

if __name__ == '__main__':
    unittest.main()

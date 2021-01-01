import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_jumps_will_exit(self):
    puzzle = puz.Puzzle()
    puzzle.process("""3
-1
""")
    puzzle.execute()
    self.assertEqual(puzzle.ip, 3)

  def test_jumps_increment_code(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1
-1
""")
    puzzle.execute()
    self.assertEqual(puzzle.jumps[0], 3)

  def test_jumps_decrement_code(self):
    puzzle = puz.Puzzle()
    puzzle.process("""0
3
0
1
-3
""")
    puzzle.execute()
    self.assertEqual(puzzle.jumps[0], 2)
    self.assertEqual(puzzle.jumps[1], 3)
    self.assertEqual(puzzle.jumps[2], 2)
    self.assertEqual(puzzle.jumps[3], 3)
    self.assertEqual(puzzle.jumps[4],-1)

if __name__ == '__main__':
    unittest.main()

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_defrag_step(self):
    puzzle = puz.Puzzle()
    puzzle.process("0 2 7 0")
    puzzle.defrag()
    self.assertEqual(puzzle.memory, [2, 4, 1, 2])

if __name__ == '__main__':
    unittest.main()

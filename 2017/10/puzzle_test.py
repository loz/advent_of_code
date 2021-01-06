import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_single_itteration(self):
    puzzle = puz.Puzzle()
    puzzle.process("3, 4, 1, 5")
    puzzle.items = [0, 1, 2, 3, 4]

    puzzle.knot()
    self.assertEqual(puzzle.items, [2, 1, 0, 3, 4])
    self.assertEqual(puzzle.cursor, 3)

  def test_wraps_around(self):
    puzzle = puz.Puzzle()
    puzzle.process("3,4,1,5")
    puzzle.items = [0, 1, 2, 3, 4]

    puzzle.knot()
    puzzle.knot()
    self.assertEqual(puzzle.items, [4, 3, 0, 1, 2])
    self.assertEqual(puzzle.cursor, 3)

  def test_example(self):
    puzzle = puz.Puzzle()
    puzzle.process("3,4,1,5")
    puzzle.items = [0, 1, 2, 3, 4]

    puzzle.encode()
    self.assertEqual(puzzle.items, [3, 4, 2, 1, 0])

  def test_can_calc_dense(self):
    puzzle = puz.Puzzle()
    self.assertEqual(puzzle.xor_chunk([65, 27, 9, 1, 4 , 3, 40, 50, 91, 7, 6, 0, 2, 5, 68, 22]), 64)

  def test_hash(self):
    puzzle = puz.Puzzle()
    self.assertEqual(puzzle.hash(""), "a2582a3a0e66e6e86e3812dcb672a272")
    self.assertEqual(puzzle.hash("AoC 2017"), "33efeb34ea91902bb2f59c9920caa6cd")
    self.assertEqual(puzzle.hash("1,2,3"), "3efbe78a8d82f29979031a4aa0b16a9d")
    self.assertEqual(puzzle.hash("1,2,4"), "63960835bcdc130f0b66d7ff4f6a5a8e")
    

if __name__ == '__main__':
    unittest.main()

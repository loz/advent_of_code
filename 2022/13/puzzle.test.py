import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_packets(self):
    puzzle = puz.Puzzle()
    puzzle.process("""[1,2,3]
[3,4,5]

[[1],[2,3,4]]
[5,[6,7,8]]

[]
[10]
""")

    p1, p2 = puzzle.packets[0]
    self.assertEquals(p1, [1,2,3])
    self.assertEquals(p2, [3,4,5])

    p1, p2 = puzzle.packets[1]
    self.assertEquals(p1, [[1],[2,3,4]])
    self.assertEquals(p2, [5, [6,7,8]])

  def test_puzzle_cmp_ints(self):
    puzzle = puz.Puzzle()

    self.assertEquals(puzzle.cmp([1], [1]), 0)
    self.assertEquals(puzzle.cmp([2], [1]), 1)
    self.assertEquals(puzzle.cmp([1], [3]), -1)

  def test_puzzle_cmp_arrays(self):
    puzzle = puz.Puzzle()

    self.assertEquals(puzzle.cmp([[1,2,3]], [[1,2,3]]), 0)
    self.assertEquals(puzzle.cmp([[2,3,4]], [[2,3,3]]), 1)
    self.assertEquals(puzzle.cmp([[2,3,3]], [[2,4,3]]), -1)

  def test_puzzle_cmp_diff_len_arrays(self):
    puzzle = puz.Puzzle()

    self.assertEquals(puzzle.cmp([[2,3]], [[2,3,3]]), -1)
    self.assertEquals(puzzle.cmp([[2,3,3]], [[2,3]]), 1)

  def test_puzzle_cmp_int_vs_array(self):
    puzzle = puz.Puzzle()

    self.assertEquals(puzzle.cmp([2], [[1]]), 1)
    self.assertEquals(puzzle.cmp([[3]],[0]), 1)

  def test_puzzle_cmp_nested(self):
    puzzle = puz.Puzzle()

    self.assertEquals(puzzle.cmp([1,[2,[3,[4,[5,6,7]]]],8,9], [1,[2,[3,[4,[5,6,0]]]],8,9]), 1)

if __name__ == '__main__':
    unittest.main()

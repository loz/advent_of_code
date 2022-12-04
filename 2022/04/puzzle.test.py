import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_ranges(self):
    puzzle = puz.Puzzle()
    puzzle.process("""2-4,6-8
""")
    pair = puzzle.pairs[0]
    left, right = pair
    self.assertEquals(left, (2,4))
    self.assertEquals(right, (6,8))

  def test_puzzle_calculates_contains(self):
    puzzle = puz.Puzzle()
    self.assertEquals(puzzle.contains((2,4),(6,8)), False)
    self.assertEquals(puzzle.contains((2,8),(3,7)), True)
    self.assertEquals(puzzle.contains((3,7),(2,8)), True)
    self.assertEquals(puzzle.contains((6,6),(4,6)), True)
    self.assertEquals(puzzle.contains((50, 90), (50, 95)), True)

  def test_puzzle_calculates_overlap(self):
    puzzle = puz.Puzzle()
    self.assertEquals(puzzle.overlaps((2,4),(6,8)), False)
    self.assertEquals(puzzle.overlaps((2,6),(5,9)),True)
    self.assertEquals(puzzle.overlaps((5,9),(2,6)),True)

    self.assertEquals(puzzle.overlaps((2,8),(3,7)), True)
    self.assertEquals(puzzle.overlaps((3,7),(2,8)), True)
    self.assertEquals(puzzle.overlaps((6,6),(4,6)), True)
    self.assertEquals(puzzle.overlaps((50, 90), (50, 95)), True)

if __name__ == '__main__':
    unittest.main()

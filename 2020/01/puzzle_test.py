import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1721
979
366
299
675
1456""")
    self.assertEquals(puzzle.sum(2020), (1721,299))

  def test_sum3(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1721
979
366
299
675
1456""")
    self.assertEquals(puzzle.sum3(2020), (979,366,675))


if __name__ == '__main__':
    unittest.main()

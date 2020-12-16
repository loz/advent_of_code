import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_gen_data(self):
    puzzle = puz.Puzzle()
    self.assertEqual(puzzle.gendata("1"), "100")
    self.assertEqual(puzzle.gendata("0"), "001")
    self.assertEqual(puzzle.gendata("11111"), "11111000000")
    self.assertEqual(puzzle.gendata("111100001010"), "1111000010100101011110000")

  def test_gen_checksum(self):
    puzzle = puz.Puzzle()
    self.assertEqual(puzzle.gencsum("10101"), "10101") #done when ODD chars
    self.assertEqual(puzzle.gencsum("110010110100"), "100")
    

if __name__ == '__main__':
    unittest.main()

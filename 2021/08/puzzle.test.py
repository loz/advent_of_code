import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_finds_bitmask_for_1(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ab ab | ab
""")
    masks = puzzle.genmasks('ab')
    mask = masks['ab']
    self.assertEqual(mask, 0b0010010)

  def test_puzzle_finds_bitmask_for_7(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ab ab | ab
""")
    masks = puzzle.genmasks('abc')
    mask = masks['abc']
    self.assertEqual(mask, 0b1010010)

  def test_puzzle_finds_bitmask_for_4(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ab ab | ab
""")
    masks = puzzle.genmasks('abcd')
    mask = masks['abcd']
    self.assertEqual(mask, 0b0111010)

  def test_puzzle_finds_bitmask_for_0(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ab ab | ab
""")
    masks = puzzle.genmasks('be fedb gbe gafceb')
    mask = masks['abcefg']
    self.assertEqual(mask, 0b1110111)

  def test_puzzle_finds_bitmask_for_3(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ab ab | ab
""")
    masks = puzzle.genmasks('be fedb gbe gedba')
    mask = masks['abdeg']
    self.assertEqual(mask, 0b1011011)

  def test_puzzle_finds_bitmask_for_2(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ab ab | ab
""")
    masks = puzzle.genmasks('be fedb gbe gafceb gedba gedca')
    mask = masks['acdeg']
    self.assertEqual(mask, 0b1011101)


  def test_puzzle_finds_bitmask_for_5(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ab ab | ab
""")
    masks = puzzle.genmasks('be fedb gbe gfdba')
    mask = masks['abdfg']
    self.assertEqual(mask, 0b1101011)

  def test_puzzle_finds_bitmask_for_6(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ab ab | ab
""")
    masks = puzzle.genmasks('be fedb gbe gfdcba')
    mask = masks['abcdfg']
    self.assertEqual(mask, 0b1101111)

  def test_puzzle_finds_bitmask_for_9(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ab ab | ab
""")
    masks = puzzle.genmasks('be fedb gbe gfedba')
    mask = masks['abdefg']
    self.assertEqual(mask, 0b1111011)

  def test_puzzle_matches_1(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ab ab | ab
""")
    first = puzzle.outputs[0]
    self.assertEqual(first, [1])


  def test_puzzle_matches_4(self):
    puzzle = puz.Puzzle()
    puzzle.process("""abcd ab | abcd
""")
    first = puzzle.outputs[0]
    self.assertEqual(first, [4])

  def test_puzzle_matches_7(self):
    puzzle = puz.Puzzle()
    puzzle.process("""abc ab | abc
""")
    first = puzzle.outputs[0]
    self.assertEqual(first, [7])

  def test_puzzle_matches_8(self):
    puzzle = puz.Puzzle()
    puzzle.process("""abcdefg ab | abcdefg
""")
    first = puzzle.outputs[0]
    self.assertEqual(first, [8])

if __name__ == '__main__':
    unittest.main()

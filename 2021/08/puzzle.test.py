import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_finds_bitmask_for_1(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ab ab | ab
""")
    masks = puzzle.genmasks('ab')
    self.assertEqual(masks[1], set(['a','b']))

  def test_puzzle_finds_bitmask_for_7(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ab ab | ab
""")
    masks = puzzle.genmasks('abc')
    self.assertEqual(masks[7], set(['a','b', 'c']))

  def test_puzzle_finds_bitmask_for_4(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ab ab | ab
""")
    masks = puzzle.genmasks('abcd')
    self.assertEqual(masks[4], set(['a','b', 'c', 'd']))

  def test_puzzle_finds_bitmask_for_8(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ab ab | ab
""")
    masks = puzzle.genmasks('abcdefg')
    self.assertEqual(masks[8], set(['a','b', 'c', 'd', 'e', 'f', 'g']))

  def test_puzzle_finds_bitmask_for_9(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ab ab | ab
""")
    masks = puzzle.genmasks('geb fedb gfecba gfedba gfdcba')
    self.assertEqual(masks[9], set(['a','b', 'd', 'e', 'f', 'g']))

  def test_puzzle_finds_bitmask_for_0(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ab ab | ab
""")
    masks = puzzle.genmasks('geb fedb gfecba gfedba gfdcba')
    self.assertEqual(masks[0], set(['a','b', 'c', 'e', 'f', 'g']))

  def test_puzzle_finds_bitmask_for_6(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ab ab | ab
""")
    masks = puzzle.genmasks('geb fedb gfecba gfedba gfdcba')
    self.assertEqual(masks[6], set(['a','b', 'c', 'd', 'f', 'g']))

  def test_puzzle_finds_bitmask_for_3(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ab ab | ab
""")
    masks = puzzle.genmasks('geb fedb gfecba gfedba gfdcba gedba gfdba gedca')
    self.assertEqual(masks[3], set(['a','b', 'd', 'e', 'g']))

  def test_puzzle_finds_bitmask_for_5(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ab ab | ab
""")
    masks = puzzle.genmasks('geb fedb gfecba gfedba gfdcba gedba gfdba gedca')
    self.assertEqual(masks[5], set(['a','b', 'd', 'f', 'g']))

  def test_puzzle_finds_bitmask_for_2(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ab ab | ab
""")
    masks = puzzle.genmasks('geb fedb gfecba gfedba gfdcba gedba gfdba gedca')
    self.assertEqual(masks[2], set(['a', 'c', 'd', 'e', 'g']))

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

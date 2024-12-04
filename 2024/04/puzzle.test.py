import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_finds_horizonal_words(self):
    puzzle = puz.Puzzle()
    puzzle.process("""AAAAAAAA
AAAAAAAA
AAAAXMAS
AAAAAAAA
""")
    self.assertEqual(((4,2),(7,2)) in puzzle.words, True)

  def test_puzzle_finds_horizonal_word_bug(self):
    puzzle = puz.Puzzle()
    puzzle.process("""ABCXXMAS
AAAAAAAA
AAAAXCAS
AAAAAAAA
""")
    self.assertEqual(((4,0),(7,0)) in puzzle.words, True)

  def test_puzzle_finds_horizonal_words_backwards(self):
    puzzle = puz.Puzzle()
    puzzle.process("""AAAAAAAA
AAAAAAAA
AAAASAMX
AAAAAAAA
""")
    self.assertEqual(((7,2),(4,2)) in puzzle.words, True)

  def test_puzzle_finds_only_consecutive_words(self):
    puzzle = puz.Puzzle()
    puzzle.process("""XMAAAAAS
AAAAAAAA
AAAAXMAS
AAAAAAAA
""")
    self.assertEqual(((4,0),(7,0)) in puzzle.words, False)

  def test_puzzle_finds_vertical_words(self):
    puzzle = puz.Puzzle()
    puzzle.process("""AAAA
BXBB
AMAA
XAAS
ASAA
CCCC
""")
    self.assertEqual(((1,1),(1,4)) in puzzle.words, True)

  def test_puzzle_finds_vertical_words_restarting(self):
    puzzle = puz.Puzzle()
    puzzle.process("""AXAA
BXBB
AMAA
XAAS
ASAA
CCCC
""")
    self.assertEqual(((1,1),(1,4)) in puzzle.words, True)

  def test_puzzle_finds_vertical_words_backwards(self):
    puzzle = puz.Puzzle()
    puzzle.process("""AAAA
BSBB
AAAA
XMAS
AXAA
CCCC
""")
    self.assertEqual(((1,4),(1,1)) in puzzle.words, True)

  def test_puzzle_finds_diagonal_words(self):
    puzzle = puz.Puzzle()
    puzzle.process("""AAAACC
BXBBCC
AMMACC
XAAACC
ASAASC
CCCCCC
""")
    self.assertEqual(((1,1),(4,4)) in puzzle.words, True)

  def test_puzzle_finds_diagonal_words_restarting(self):
    puzzle = puz.Puzzle()
    puzzle.process("""XAAACC
BXBBCC
AMMACC
XAAACC
ASAASC
CCCCCC
""")
    self.assertEqual(((1,1),(4,4)) in puzzle.words, True)

  def test_puzzle_finds_diagonal_words_backwards(self):
    puzzle = puz.Puzzle()
    puzzle.process("""AAAACC
BSBBCC
AMAACC
XAAMCC
ASAAXC
CCCCCC
""")
    self.assertEqual(((4,4),(1,1)) in puzzle.words, True)

  def test_puzzle_finds_diagonal_words_forward_slash(self):
    puzzle = puz.Puzzle()
    puzzle.process("""AAAACC
BSBBSC
AMAACC
XAMMCC
AXAAXC
CCCCCC
""")
    self.assertEqual(((1,4),(4,1)) in puzzle.words, True)

  def test_puzzle_finds_diagonal_words_forward_slash(self):
    puzzle = puz.Puzzle()
    puzzle.process("""
XMASAMX
MM...MM
A.A.A.A
S..S..S
A.A.A.A
MM...MM
XMASAMX
""")
    self.assertEqual(len(puzzle.words), 12)
    
if __name__ == '__main__':
    unittest.main()

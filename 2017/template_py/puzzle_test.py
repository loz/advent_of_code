import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle(self):
    puzzle = puz.Puzzle()
    puzzle.process("""inputhere
""")
    pass

if __name__ == '__main__':
    unittest.main()

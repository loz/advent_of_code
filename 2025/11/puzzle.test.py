import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_graph(self):
    puzzle = puz.Puzzle()
    puzzle.process("""aaa: bbb ccc
bbb: ccc
ccc: ddd eee
ddd: fff
eee: fff
""")

    self.assertIn('bbb', puzzle.graph['aaa'])
    self.assertIn('ccc', puzzle.graph['aaa'])
    self.assertIn('fff', puzzle.graph['eee'])

if __name__ == '__main__':
    unittest.main(verbosity=2)

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_network(self):
    puzzle = puz.Puzzle()
    puzzle.process("""aa-bb
bb-cc
dd-aa
""")

    anode = puzzle.nodes('aa')
    self.assertIn('bb', anode)
    self.assertIn('dd', anode)
    self.assertEqual(len(anode), 2)


  """
    aa-bb-cc-dd
     |  |  |  |
     +--+-ee+-+
    aa,bb,ee
    bb-cc-ee
    cc-dd-ee
  """
  def test_finds_trios(self):
    puzzle = puz.Puzzle()
    puzzle.process("""aa-bb
aa-ee
bb-cc
bb-ee
cc-dd
dd-ee
cc-ee
""")

    trios = puzzle.find_trios()
    self.assertIn(set(['aa', 'bb', 'ee']), trios)
    self.assertIn(set(['bb', 'cc', 'ee']), trios)
    self.assertIn(set(['cc', 'dd', 'ee']), trios)
    self.assertEqual(len(trios), 3)
    


if __name__ == '__main__':
    unittest.main(verbosity=2)

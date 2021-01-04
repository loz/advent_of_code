import unittest
import puzzle as puz

EXAMPLE="""pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
"""

class TestPuzzle(unittest.TestCase):

  def test_parses_links_and_number(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)
  
    nid, children = puzzle.nodes['tknk']
    self.assertEqual(nid, 41)
    self.assertEqual(children, ['ugml', 'padx', 'fwft'])

  def test_can_locate_root_node(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)
    self.assertEqual(puzzle.find_root(), 'tknk')

if __name__ == '__main__':
    unittest.main()

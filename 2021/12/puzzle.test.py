import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_buids_map(self):
    puzzle = puz.Puzzle()
    puzzle.process("""start-A
start-B
A-end
B-end
""")
    self.assertEqual(puzzle.nodes['start'], set(['A', 'B']))
    self.assertEqual(puzzle.nodes['A'], set(['start', 'end']))
    self.assertEqual(puzzle.nodes['B'], set(['start', 'end']))
    self.assertEqual(puzzle.nodes['end'], set(['A', 'B']))

  def test_puzzle_builds_paths(self):
    puzzle = puz.Puzzle()
    puzzle.process("""start-A
start-b
A-c
A-b
b-d
A-end
b-end
""")
    paths = puzzle.build_paths()
    self.assertEqual(len(paths), 36)
if __name__ == '__main__':
    unittest.main()

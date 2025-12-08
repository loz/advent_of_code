import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_coords(self):
    puzzle = puz.Puzzle()
    puzzle.process("""123,345,678
111,222,333
444,555,666
""")

    coords = puzzle.coords
    self.assertEqual(len(coords), 3)
    self.assertIn((123,345,678), coords)
    self.assertIn((111,222,333), coords)
    self.assertIn((444,555,666), coords)

  def test_pairs_junctions(self):
    puzzle = puz.Puzzle()

    boxes = [(162,817,812), (984,92,344), (425,690,689)]

    pairs = puzzle.pair_junctions(boxes)

    self.assertIn(((162,817,812), (425,690,689)), pairs)
    self.assertIn(((984,92,344), (425,690,689)), pairs)
    self.assertIn(((162,817,812), (984,92,344)), pairs)

if __name__ == '__main__':
    unittest.main(verbosity=2)

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_gets_shapes_and_regions(self):
    puzzle = puz.Puzzle()
    puzzle.process("""0:
##
#.


2:
##
..


10x10: 0 0 0 0 2 0
12x8: 1 0 1 0 2 2
11x9: 0 1 0 1 2 3
""")

    self.assertEqual(len(puzzle.shapes), 2)
    self.assertEqual(len(puzzle.regions), 3)

    shape = puzzle.get_shape(0)
    self.assertEqual("##", shape[0])
    self.assertEqual("#.", shape[1])

    region = puzzle.regions[0]
    size, presents = region
    self.assertEqual((10,10), size)
    self.assertEqual([0, 0, 0, 0, 2, 0], presents)


  def test_puzzle_get_shape_permutaions(self):
    puzzle = puz.Puzzle()

    puzzle.process("""0:
##
#.


2:
##
..


10x10: 0 0 0 0 2 0
12x8: 1 0 1 0 2 2
11x9: 0 1 0 1 2 3
""")
    variants = puzzle.get_permutations(2)

    self.assertEqual(len(variants), 4)
    self.assertIn(['##','..'], variants)
    self.assertIn(['.#','.#'], variants)
    self.assertIn(['#.','#.'], variants)
    self.assertIn(['..','##'], variants)


if __name__ == '__main__':
    unittest.main(verbosity=2)

import unittest
import puzzle as puz

EXAMPLE="""###########
#0.1.....2#
#.#######.#
#4.......3#
###########
"""

class TestPuzzle(unittest.TestCase):

  def test_puzzle_locates_markers(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)
    
    markers = puzzle.markers
    self.assertEqual(len(markers), 5)
    self.assertEqual(markers[0], (1,1))
    self.assertEqual(markers[1], (3,1))
    self.assertEqual(markers[2], (9,1))
    self.assertEqual(markers[3], (9,3))
    self.assertEqual(markers[4], (1,3))

if __name__ == '__main__':
    unittest.main()

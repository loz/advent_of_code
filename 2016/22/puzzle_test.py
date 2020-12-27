import unittest
import puzzle as puz

EXAMPLE="""root@ebhq-gridcenter# df -h
Filesystem              Size  Used  Avail  Use%
/dev/grid/node-x0-y0     89T   65T    24T   73%
/dev/grid/node-x0-y1     92T   64T    28T   69%
/dev/grid/node-x0-y2     85T   70T    15T   82%
/dev/grid/node-x0-y3     90T   64T    26T   71%
"""

class TestPuzzle(unittest.TestCase):

  def test_parses_grid(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)

    self.assertEqual(puzzle.grid(0,0)['size'], 89)
    self.assertEqual(puzzle.grid(0,2)['used'], 70)
    self.assertEqual(puzzle.grid(0,3)['avail'],26)

if __name__ == '__main__':
    unittest.main()

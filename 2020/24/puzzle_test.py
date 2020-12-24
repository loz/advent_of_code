import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_parse_directions(self):
    puzzle = puz.Puzzle()
    puzzle.process("""sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
nwwswee
esew
""")
    self.assertEqual(puzzle.directions[0], ['se', 'se', 'nw', 'ne', 'ne', 'ne', 'w', 'se', 'e', 'sw', 'w', 'sw', 'sw', 'w', 'ne', 'ne', 'w', 'se', 'w', 'sw'])

  def test_follows_and_flips_east(self):
    puzzle = puz.Puzzle()
    puzzle.process("""eee""")

    self.assertEqual(puzzle.tile_at( 3,0), 'black')

  def test_follows_and_flips_west(self):
    puzzle = puz.Puzzle()
    puzzle.process("""www""")

    self.assertEqual(puzzle.tile_at(-3,0), 'black')

  def test_follows_and_flips_nwest(self):
    puzzle = puz.Puzzle()
    puzzle.process("""nwnwnw""")
    """
( 0,-1)
(-1,-1)
( 0,-1)
=======
(-1,-3)
"""
    self.assertEqual(puzzle.tile_at(-1,-3), 'black')
    
  def test_follows_and_flips_neast(self):
    puzzle = puz.Puzzle()
    puzzle.process("""nenene""")
    """
( 1,-1)
( 0,-1)
( 1,-1)
=======
( 2,-3)
"""
    self.assertEqual(puzzle.tile_at(2,-3), 'black')

  def test_follows_and_flips_swest(self):
    puzzle = puz.Puzzle()
    puzzle.process("""swswsw""")
    """
( 0, 1)
(-1, 1)
( 0, 1)
=======
(-1, 3)
"""
    self.assertEqual(puzzle.tile_at(-1, 3), 'black')

  def test_follows_and_flips_seast(self):
    puzzle = puz.Puzzle()
    puzzle.process("""sesese""")
    """
( 1, 1)
( 0, 1)
( 1, 1)
=======
( 2, 3)
"""
    self.assertEqual(puzzle.tile_at(2, 3), 'black')

  def test_directions_reversable(self):
    puzzle = puz.Puzzle()
    puzzle.process("""nwwswee""")
    self.assertEqual(puzzle.tile_at(0, 0), 'black')

if __name__ == '__main__':
    unittest.main()

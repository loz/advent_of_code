import unittest
import puzzle as puz

EXAMPLE="""Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
"""

class TestPuzzle(unittest.TestCase):

  def test_parses_tiles(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)

    self.assertEqual(puzzle.tiles[2729], """...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.
""")

  def test_identifies_edges(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)

    self.assertEqual(puzzle.edges[2473], ['#....####.','####...##.','...###.#..','..###.#.#.'])

  def test_matches_edges(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)
    """
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Matched version is vertically flipped version
matches on its 'top' and right'

"""
    matches = puzzle.matches(1951)
    expected = [
      [(2729,3)],#top -> 2729:bottom
      [],#left
      [(2311,1)],#right -> 2311:left
      [],#bottom
    ]
    self.assertEqual(matches,expected)

  def test_assembles_map(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)
    
    mapimg = puzzle.assemble_map()
    expected = """.#.#..#.##...#.##..#####
###....#.#....#..#......
##.##.###.#.#..######...
###.#####...#.#####.#..#
##.#....#.##.####...#.##
...########.#....#####.#
....#..#...##..#.#.###..
.####...#..#.....#......
#..#.##..#..###.#.##....
#.####..#.####.#.#.###..
###.#.#...#.######.#..##
#.####....##..########.#
##..##.#...#...#.#.#.#..
...#..#..#.#.##..###.###
.#.#....#.##.#...###.##.
###.#...#..#.##.######..
.#.#.###.##.##.#..#.##..
.####.###.#...###.#..#.#
..#.#..#..#.#.#.####.###
#..####...#.#.#.###.###.
#####..#####...###....##
#.##..#..#...#..####...#
.#.###..##..##..####.##.
...###...##...#...#..###
"""
    print '====== MAPIMG ======='
    print mapimg
    print '===================='
    #Order not guarenteed, so expected could be HMirror or VMirror or Rot90 RMirror, VMirror
    matched = False
    #print mapimg
    if mapimg == expected:
      matched = True
    hmirror = puzzle.hmirror(mapimg)
    #print hmirror
    if hmirror == expected:
      matched = True
    vmirror = puzzle.vmirror(mapimg)
    #print vmirror
    if vmirror == expected:
      matched = True
    hvmirror = puzzle.hmirror(vmirror)
    #print hvmirror
    if hvmirror == expected:
      matched = True

    mapimg = puzzle.rotate(mapimg)
    #print mapimg
    if mapimg == expected:
      matched = True
    hmirror = puzzle.hmirror(mapimg)
    #print hmirror
    if hmirror == expected:
      matched = True
    vmirror = puzzle.vmirror(mapimg)
    #print vmirror
    if vmirror == expected:
      matched = True
    hvmirror = puzzle.hmirror(vmirror)
    #print hvmirror
    if hvmirror == expected:
      matched = True

    self.assertTrue(matched)
    

if __name__ == '__main__':
    unittest.main()

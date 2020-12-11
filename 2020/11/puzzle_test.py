import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_empty_no_adjacent_gets_occupied(self):
    puzzle = puz.Puzzle()
    puzzle.process("""...
.L.
...
""")
    puzzle.tick()
    state = puzzle.toString()
    self.assertEqual(state, """...
.#.
...""")

  def test_occupied_by_four_empties(self):
    puzzle = puz.Puzzle()
    puzzle.process("""L...
L.#.
.###
.L#.
""")
    puzzle.tick()
    state = puzzle.toString()
    self.assertEqual(state, """#...
L.#.
.#L#
.L#.""")

  def test_both_apply_at_same_time(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".#.
###
.#.
""")
    puzzle.tick()
    state = puzzle.toString()
    self.assertEqual(state, """.#.
#L#
.#.""")

  def test_new_neighbors_method(self):
    puzzle = puz.Puzzle()
    puzzle.process("""
.......#.
...#.....
.L.......
.........
..#L....#
....#....
.........
#........
...L.....""")
    neighbours = puzzle.neighbours(3,4)
    neighbours.sort()
    self.assertEqual(''.join(neighbours), '######LL')

  def test_new_neighbors_method_example2(self):
    puzzle = puz.Puzzle()
    puzzle.process("""
.............
.L.L.#.#.#.#.
.............
""")
    neighbours = puzzle.neighbours(1,1)
    neighbours.sort()
    self.assertEqual(''.join(neighbours), 'L')

  def test_new_neighbors_method_example3(self):
    puzzle = puz.Puzzle()
    puzzle.process("""
.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##.
""")
    neighbours = puzzle.neighbours(3,3)
    neighbours.sort()
    self.assertEqual(''.join(neighbours), '')

if __name__ == '__main__':
    unittest.main()

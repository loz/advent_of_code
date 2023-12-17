import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_map(self):
    puzzle = puz.Puzzle()
    puzzle.process("""123
456
789
""")
    self.assertEqual(puzzle.at(1,1), 5)
    self.assertEqual(puzzle.at(2,2), 9)

  def test_puzzle_neighbours_gives_options(self):
    puzzle = puz.Puzzle()
    puzzle.process("""123
456
789
""")
    nbrs = puzzle.neighbours(1,1)
    self.assertEqual(((0,1), (-1, 0)) in nbrs, True)
    self.assertEqual(((2,1), ( 1, 0)) in nbrs, True)
    self.assertEqual(((1,0), (0, -1)) in nbrs, True)
    self.assertEqual(((1,2), (0,  1)) in nbrs, True)


  def test_puzzle_ultra_neighbours_gives_4_moves_for_empty_history(self):
    puzzle = puz.Puzzle()
    puzzle.process("""123
456
789
""")
    nbrs = puzzle.ultra_neighbours((1, 1), [])
    self.assertEqual(((0,1), (-1, 0)) in nbrs, True)
    self.assertEqual(((2,1), ( 1, 0)) in nbrs, True)
    self.assertEqual(((1,0), (0, -1)) in nbrs, True)
    self.assertEqual(((1,2), (0,  1)) in nbrs, True)

  def test_puzzle_ultra_neighbours_gives_same_direction_for_less_than_4_same(self):
    puzzle = puz.Puzzle()
    puzzle.process("""123
456
789
""")
    nbrs = puzzle.ultra_neighbours((1, 1), [(0, 1)])
    self.assertEqual(((1,2), (0,  1)) in nbrs, True)
    self.assertEqual(len(nbrs), 1)

    nbrs = puzzle.ultra_neighbours((1, 1), [(0, 1), (0, 1)])
    self.assertEqual(((1,2), (0,  1)) in nbrs, True)
    self.assertEqual(len(nbrs), 1)

    nbrs = puzzle.ultra_neighbours((1, 1), [(0, 1), (0, 1), (0, 1)])
    self.assertEqual(((1,2), (0,  1)) in nbrs, True)
    self.assertEqual(len(nbrs), 1)

    nbrs = puzzle.ultra_neighbours((1, 1), [(1, 0), (0, 1), (0, 1), (0, 1)])
    self.assertEqual(((1,2), (0,  1)) in nbrs, True)
    self.assertEqual(len(nbrs), 1)

  def test_puzzle_ultra_neighbours_changes_90direction_after_10_same(self):
    puzzle = puz.Puzzle()
    puzzle.process("""123
456
789
""")

    nbrs = puzzle.ultra_neighbours((1, 1), [(0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1)])
    self.assertEqual(((1,2), (0,  1)) in nbrs, False)
    self.assertEqual(((0,1), (-1, 0)) in nbrs, True)
    self.assertEqual(((2,1), (1, 0)) in nbrs, True)
    self.assertEqual(len(nbrs), 2)

  def test_puzzle_ultra_neighbours_can_change_after_4same(self):
    puzzle = puz.Puzzle()
    puzzle.process("""123
456
789
""")

    nbrs = puzzle.ultra_neighbours((1, 1), [(0, 1), (0, 1), (0, 1), (0, 1)])
    self.assertEqual(((1,2), (0,  1)) in nbrs, True)
    self.assertEqual(((0,1), (-1, 0)) in nbrs, True)
    self.assertEqual(((2,1), (1, 0)) in nbrs, True)
    self.assertEqual(len(nbrs), 3)

    nbrs = puzzle.ultra_neighbours((1, 1), [(0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (1, 0), (0, 1), (0, 1), (0, 1), (0, 1)])
    self.assertEqual(((1,2), (0,  1)) in nbrs, True)
    self.assertEqual(((0,1), (-1, 0)) in nbrs, True)
    self.assertEqual(((2,1), (1, 0)) in nbrs, True)
    self.assertEqual(len(nbrs), 3)

  def test_moves_generates_range_of_moves(self):
    puzzle = puz.Puzzle()
    puzzle.process("""123
456
789
""")

    moves = puzzle.moves((0, 0), 'v', 1,2)
    self.assertEqual(len(moves), 2)
    self.assertEqual(((1,0), 2, 'h') in moves, True)
    self.assertEqual(((2,0), 5, 'h') in moves, True)

    moves = puzzle.moves((0, 0), 'h', 1,2)
    self.assertEqual(len(moves), 2)
    self.assertEqual(((0,1), 4, 'v') in moves, True)
    self.assertEqual(((0,2), 11, 'v') in moves, True)


if __name__ == '__main__':
    unittest.main()

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_map(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi""")

    self.assertEquals(puzzle.map(0,0), 'S')
    self.assertEquals(puzzle.map(5,2), 'E')
    self.assertEquals(puzzle.map(4,4), 'f')
    self.assertEquals(puzzle.map(3,3), 't')

  def test_puzzle_parses_start_and_end(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi""")

    self.assertEquals(puzzle.start, (0,0))
    self.assertEquals(puzzle.end, (5,2))

  def test_puzzle_can_move_same_level(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Saaaa
aaxaa
aaaaa
aaxaa""")

    moves = puzzle.moves_from(2, 2)
    self.assertEquals((1,2) in moves, True)
    self.assertEquals((3,2) in moves, True)
    self.assertEquals(len(moves), 2)

  def test_puzzle_can_move_up_at_most_one(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Sbaxa
aabaa
aaaaa
aabaa""")

    moves = puzzle.moves_from(2, 0)
    self.assertEquals((1,0) in moves, True)
    self.assertEquals((2,1) in moves, True)
    self.assertEquals(len(moves), 2)

  def test_puzzle_can_move_down_any_height(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Sbaxa
aabza
aaaaa
aabaa""")

    moves = puzzle.moves_from(3, 0)
    self.assertEquals((2,0) in moves, True)
    self.assertEquals((4,0) in moves, True)
    self.assertEquals(len(moves), 2)

  def test_puzzle_start_is_a(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Sbaxa
aabza
aaaaa
aabaa""")

    moves = puzzle.moves_from(0, 0)
    self.assertEquals((1,0) in moves, True)
    self.assertEquals((0,1) in moves, True)
    self.assertEquals(len(moves), 2)

  def test_puzzle_end_is_z(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Sbaxa
aabza
aaaEa
aabaa""")

    moves = puzzle.moves_from(3, 1)
    self.assertEquals((3,2) in moves, True)

if __name__ == '__main__':
    unittest.main()

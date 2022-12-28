import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_map(self):
    puzzle = puz.Puzzle()
    puzzle.process("""#######
#.G.E.#
#E.G.E#
#.G.E.#
#######
""")

    self.assertEquals(puzzle.item_at(0,0), '#')
    self.assertEquals(puzzle.item_at(1,1), '.')
    g = puzzle.item_at(2,1)
    e = puzzle.item_at(4,3)
    self.assertEquals(isinstance(g, puz.Goblin), True)
    self.assertEquals(isinstance(e, puz.Elf), True)

  def test_open_squares_for_goblin(self):
    puzzle = puz.Puzzle()
    puzzle.process("""#######
#.G.E.#
#E.G.E#
#.G.E.#
#######
""")

    g = puzzle.item_at(2,1)
    squares = g.open_squares()
    self.assertEquals((1,1) in squares, True)
    self.assertEquals((3,1) in squares, True)
    self.assertEquals((2,2) in squares, True)
    self.assertEquals((0,2) in squares, False)

  def test_move_goes_to_closest_enemy(self):
    puzzle = puz.Puzzle()
    puzzle.process("""#######
#.G.E.#
#.....#
#.G.E.#
#######
""")

    e = puzzle.elves[(4,1)]
    move = e.gen_move()
    self.assertEquals(move, (3,1))

  def test_blocked_does_not_move(self):
    puzzle = puz.Puzzle()
    puzzle.process("""#######
#.G.E.#
#...#.#
#.G.#E#
#######
""")

    e = puzzle.elves[(5,3)]
    move = e.gen_move()
    self.assertEquals(move, None)

if __name__ == '__main__':
    unittest.main()

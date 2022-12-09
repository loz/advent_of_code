import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_centers_virus_on_map(self):
    puzzle = puz.Puzzle()
    puzzle.process("""..#
#..
...
""")

    self.assertEquals(puzzle.virus.pos, (0,0))
    self.assertEquals(puzzle.virus.dir, 'UP')
    self.assertEquals(puzzle.nodeAt(-1,0), '#')

  def test_puzzle_infected_node_turns_right(self):
    puzzle = puz.Puzzle()
    puzzle.process("""..#
##.
...
""")
    puzzle.burst()
    self.assertEquals(puzzle.virus.dir, 'RT')

  def test_puzzle_clean_node_turns_left(self):
    puzzle = puz.Puzzle()
    puzzle.process("""..#
#..
...
""")
    puzzle.burst()
    self.assertEquals(puzzle.virus.dir, 'LT')

  def test_puzzle_right_turns_down(self):
    puzzle = puz.Puzzle()
    puzzle.process("""..#
##.
.#.""")
    puzzle.virus.dir = 'RT'
    puzzle.burst()
    self.assertEquals(puzzle.virus.dir, 'DN')
    self.assertEquals(puzzle.virus.pos, (0, 1))

  def test_puzzle_down_turns_left(self):
    puzzle = puz.Puzzle()
    puzzle.process("""..#
##.
.#.""")
    puzzle.virus.dir = 'DN'
    puzzle.burst()
    self.assertEquals(puzzle.virus.dir, 'LT')
    self.assertEquals(puzzle.virus.pos, (-1, 0))

  def test_puzzle_left_turns_up(self):
    puzzle = puz.Puzzle()
    puzzle.process("""..#
##.
.#.""")
    puzzle.virus.dir = 'LT'
    puzzle.burst()
    self.assertEquals(puzzle.virus.dir, 'UP')
    self.assertEquals(puzzle.virus.pos, (0, -1))

  def test_puzzle_clean_node_infects(self):
    puzzle = puz.Puzzle()
    puzzle.process("""..#
#..
...""")
    puzzle.burst()
    self.assertEquals(puzzle.nodeAt(0,0), '#')

  def test_puzzle_infected_node_cleaned(self):
    puzzle = puz.Puzzle()
    puzzle.process("""..#
##.
...""")
    puzzle.burst()
    self.assertEquals(puzzle.nodeAt(0,0), None)

  def test_puzzle_virus_moves(self):
    puzzle = puz.Puzzle()
    puzzle.process("""..#
##.
...""")
    puzzle.burst()
    self.assertEquals(puzzle.virus.pos, (1, 0))

if __name__ == '__main__':
    unittest.main()

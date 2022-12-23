import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_scans_elf_locations(self):
    puzzle = puz.Puzzle()
    puzzle.process("""...
..#
#..
""")
    
    self.assertEquals(puzzle.elf_at(0,0), False)
    self.assertEquals(puzzle.elf_at(2,1), True)
    self.assertEquals(puzzle.elf_at(0,2), True)
    self.assertEquals(puzzle.elf_at(2,2), False)

  def test_puzzle_lone_elf_does_not_move(self):
    puzzle = puz.Puzzle()
    puzzle.process("""...
.#.
...
""")
    puzzle.tick()
    self.assertEquals(puzzle.elf_at(1,1), True)

  def test_puzzle_no_n_ne_nw_goes_north(self):
    puzzle = puz.Puzzle()
    puzzle.process("""...
.#.
..#
""")
    puzzle.tick()
    self.assertEquals(puzzle.elf_at(1,0), True)

  def test_puzzle_no_s_se_sw_goes_south(self):
    puzzle = puz.Puzzle()
    puzzle.process("""..#
.#.
...
""")
    puzzle.tick()
    self.assertEquals(puzzle.elf_at(1,2), True)

  def test_puzzle_no_w_nw_sw_goes_west(self):
    puzzle = puz.Puzzle()
    puzzle.process("""..#
.#.
..#
""")
    puzzle.tick()
    self.assertEquals(puzzle.elf_at(0,1), True)

  def test_puzzle_no_e_ne_se_goes_east(self):
    puzzle = puz.Puzzle()
    puzzle.process("""#..
.#.
#..
""")
    puzzle.tick()
    self.assertEquals(puzzle.elf_at(2,1), True)

if __name__ == '__main__':
    unittest.main()

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_rocks(self):
    puzzle = puz.Puzzle()
    puzzle.process("""O.#.
.O..
#.O.
""")
  
    self.assertEqual(puzzle.at(0,0), 'O')
    self.assertEqual(puzzle.at(0,2), '#')

  def test_puzzle_rocks_roll_north(self):
    puzzle = puz.Puzzle()
    puzzle.process("""O.#.
.O..
#.O.
""")
  
    puzzle.rollNorth()

    self.assertEqual(puzzle.at(0,0), 'O')
    self.assertEqual(puzzle.at(1,0), 'O')
    self.assertEqual(puzzle.at(2,1), 'O')

  def test_puzzle_rocks_roll_east(self):
    puzzle = puz.Puzzle()
    puzzle.process("""O.#.
.O..
#.O.
""")
  
    puzzle.rollEast()

    self.assertEqual(puzzle.at(1,0), 'O')
    self.assertEqual(puzzle.at(3,1), 'O')
    self.assertEqual(puzzle.at(3,2), 'O')

  def test_puzzle_rocks_roll_south(self):
    puzzle = puz.Puzzle()
    puzzle.process("""O.#.
.O..
#.O.
""")
  
    puzzle.rollSouth()

    self.assertEqual(puzzle.at(0,1), 'O')
    self.assertEqual(puzzle.at(1,2), 'O')
    self.assertEqual(puzzle.at(2,2), 'O')

  def test_puzzle_rocks_roll_west(self):
    puzzle = puz.Puzzle()
    puzzle.process("""O.#.
.O..
#.O.
""")
  
    puzzle.rollWest()

    self.assertEqual(puzzle.at(0,0), 'O')
    self.assertEqual(puzzle.at(0,1), 'O')
    self.assertEqual(puzzle.at(1,2), 'O')




if __name__ == '__main__':
    unittest.main()

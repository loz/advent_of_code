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




if __name__ == '__main__':
    unittest.main()

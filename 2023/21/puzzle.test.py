import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_processes_map(self):
    puzzle = puz.Puzzle()
    puzzle.process("""....
.#..
.#S.
...#
""")
  
    
    self.assertEqual(puzzle.at(1,1), '#')

  def test_puzzle_identifies_start(self):
    puzzle = puz.Puzzle()
    puzzle.process("""....
.#..
.#S.
...#
""")
  
    
    self.assertEqual(puzzle.at(2,2), '.')
    self.assertEqual(puzzle.start, (2,2))

  def test_puzzle_walks_distance(self):
    puzzle = puz.Puzzle()
    puzzle.process("""....
.#..
.#S.
...#
""")
    #
    # [(2, 1), (3, 1), (2, 0), (2, 3), (2, 2), (3, 2), (1, 3)]
    #
    # ..O.
    # .#.O
    # .#O.
    # .O.#
    
    start = puzzle.start
    spaces = puzzle.walk(start, 2)
    self.assertEqual((2,2) in spaces, True)
    self.assertEqual((3,1) in spaces, True)
    self.assertEqual((2,0) in spaces, True)
    self.assertEqual((1,3) in spaces, True)
    self.assertEqual(len(spaces), 4)



if __name__ == '__main__':
    unittest.main()

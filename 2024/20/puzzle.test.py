import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_maze(self):
    puzzle = puz.Puzzle()
    puzzle.process("""######
#S ###
## ###
##  E#
######
""")

    
    self.assertIn((0,0), puzzle.walls)
    self.assertIn((1,2), puzzle.walls)
    self.assertIn((4,2), puzzle.walls)
    self.assertIn((3,4), puzzle.walls)

    self.assertEqual(puzzle.width, 6)
    self.assertEqual(puzzle.height, 5)

    self.assertEqual(puzzle.start, (1,1))
    self.assertEqual(puzzle.end, (4, 3))

  def test_puzzle_solves_maze(self):
    puzzle = puz.Puzzle()
    puzzle.process("""######
#S ###
## ###
##  E#
######
""")

    path = puzzle.solve()
    
    self.assertEqual(path, [
      (1,1), (2, 1), (2,2), (2,3), (3,3), (4,3)
    ])


  def test_puzzle_finds_cheats(self):
    puzzle = puz.Puzzle()
    puzzle.process("""#####    
#S#E#
# # #
#   #
#####
""")

    path = puzzle.solve()
    
    cheats = puzzle.find_cheats(path)

    self.assertEqual(len(cheats), 2)
    #( saving, start, end)
    self.assertIn( (4, (2,1), (3,1) ) , cheats)
    self.assertIn( (2, (2,2), (3,2) ) , cheats)


  #Test Case Required...
  """
  Is this possible in a maze?

  ######
  #S##E#  S12E
  #    #
  ######
  """
  def test_puzzle_finds_cheats_with_distance(self):
    puzzle = puz.Puzzle()
    puzzle.process("""######
#S##E#
# ## #
#    #
######
""")

    path = puzzle.solve()
    cheats = puzzle.find_cheats_with_distance(path,4)
    """
      nocheat for 7

#((2, 1), (4, 1)) saving 4
      S->E shortest, lots of waste available 
           cheat is 2, saving 7

#((1, 0), (4, 1)) saving 2
      ^>>v
      S  E

#((2, 2), (4, 1)) saving 2
      S >E
      +-^  cheat is 3 (or ^>), saving 2

#((2, 2), (4, 2)) saving 2
      S  E
      +->^ cheat is 2, saving 2

#((2, 1), (4, 2)) saving 2
      Sv E
       >>^ cheat is 2, saving 2
    """
    self.assertEqual(len(cheats), 5)
    #( saving, start, end)
    self.assertIn( (4, (2,1), (4,1) ) , cheats)
    self.assertIn( (2, (2,2), (4,1) ) , cheats)
    self.assertIn( (2, (1,0), (4,1) ) , cheats)
    self.assertIn( (2, (2,2), (4,2) ) , cheats)
    self.assertIn( (2, (2,1), (4,2) ) , cheats)


  def test_puzzle_cheats_can_go_in_and_out_of_walls(self):
    self.assertTrue(False)

if __name__ == '__main__':
    unittest.main(verbosity=2)

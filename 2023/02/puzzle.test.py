import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_game_has_id(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Game 9: 2 blue, 3 red; 4 green, 5 red; 3 red, 5 blue
""")
    self.assertEqual(puzzle.games[0].id, 9)

  def test_puzzle_game_has_rounds(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Game 9: 2 blue, 3 red; 4 green, 5 red; 3 red, 5 blue
""")
    self.assertEqual(puzzle.games[0].rounds[0], [('blue',2), ('red',3)])

  def test_puzzle_game_possible_with_more_colours(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Game 9: 2 blue, 3 red; 4 green, 5 red; 3 red, 5 blue
""")
    game = puzzle.games[0]
    self.assertEqual(game.possible({'red':5, 'green':5, 'blue':5}), True)

  def test_puzzle_game_impossible_with_too_few_blue(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Game 9: 2 blue, 3 red; 4 green, 5 red; 3 red, 5 blue
""")
    game = puzzle.games[0]
    self.assertEqual(game.possible({'red':5, 'green':5, 'blue':4}), False)

  def test_puzzle_game_impossible_with_too_few_red(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Game 9: 2 blue, 3 red; 4 green, 5 red; 3 red, 5 blue
""")
    game = puzzle.games[0]
    self.assertEqual(game.possible({'red':4, 'green':4, 'blue':5}), False)

  def test_puzzle_game_impossible_with_too_few_green(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Game 9: 2 blue, 3 red; 4 green, 5 red; 3 red, 5 blue
""")
    game = puzzle.games[0]
    self.assertEqual(game.possible({'red':5, 'green':3, 'blue':5}), False)

  def test_puzzle_game_can_pull_same_colours_in_set(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Game 9: 3 red, 3 red; 4 green, 5 red; 3 red, 5 blue
""")
    game = puzzle.games[0]
    self.assertEqual(game.possible({'red':6, 'green':4, 'blue':5}), True)
    self.assertEqual(game.possible({'red':5, 'green':4, 'blue':5}), False)


  def test_puzzle_min_cubes(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Game 9: 3 red, 3 red; 4 green, 5 red; 3 red, 5 blue
""")
    game = puzzle.games[0]
    self.assertEqual(game.mincubes(), {'red':6, 'green':4, 'blue':5})

if __name__ == '__main__':
    unittest.main()

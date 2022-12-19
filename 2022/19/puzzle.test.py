import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_blueprints(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 10 clay. Each geode robot costs 4 ore and 10 obsidian.
""")

    blueprint = puzzle.blueprints[0]

    self.assertEquals(blueprint, {
      "ore":(4,0,0),
      "clay":(3,0,0),
      "obsidian":(2,10,0),
      "geode":(4,0,10)
      })

  def test_puzzle_gen_choices_ore_clay_or_none(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 10 clay. Each geode robot costs 4 ore and 10 obsidian.
""")

    blueprint = 0
    resources = (3,0,0,0)
    choices = puzzle.gen_choices(blueprint, resources)

    self.assertEquals(choices, ['clay', None])

  def test_puzzle_gen_choices_ore_clay_and_ore_or_none(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 10 clay. Each geode robot costs 4 ore and 10 obsidian.
""")

    blueprint = 0
    resources = (4,0,0,0)
    choices = puzzle.gen_choices(blueprint, resources)

    self.assertEquals(choices, ['ore', 'clay', None])

  def test_puzzle_gen_clay_for_ob_robot_waits_for_rest(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 6 ore and 10 clay. Each geode robot costs 4 ore and 10 obsidian.
""")

    blueprint = 0
    resources = (5,10,0,0)
    choices = puzzle.gen_choices(blueprint, resources)

    self.assertEquals(choices, [None])

  def test_puzzle_gen_obs_for_geo_robot_waits_for_rest(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 10 clay. Each geode robot costs 4 ore and 10 obsidian.
""")

    blueprint = 0
    resources = (3,10,10,0)
    choices = puzzle.gen_choices(blueprint, resources)

    self.assertEquals(choices, [None])

if __name__ == '__main__':
    unittest.main()

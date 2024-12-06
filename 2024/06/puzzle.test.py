import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_obstacles(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".....
.#...
.^.#.
.#...
....#
""")
    self.assertEqual(len(puzzle.obstacles), 4)
    self.assertIn((1,1), puzzle.obstacles)
    self.assertIn((1,3), puzzle.obstacles)
    self.assertIn((3,2), puzzle.obstacles)
    self.assertIn((4,4), puzzle.obstacles)

  def test_puzzle_locates_guard(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".....
.#...
.^.#.
.#...
....#
""")
    self.assertEqual(puzzle.guard_location, (1,2, '^'))

  def test_puzzle_guard_moves_up_until_obstacle(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".....
.#...
...#.
.....
.^..#
""")

    self.assertEqual(puzzle.guard_location, (1,4, '^'))
    for i in range(2):
      puzzle.move_guard()
    self.assertEqual(puzzle.guard_location, (1,2, '^'))

  def test_puzzle_guard_turns_right_at_obstacle(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".....
.#...
...#.
.....
.^..#
""")

    for i in range(3):
      puzzle.move_guard()
    self.assertEqual(puzzle.guard_location, (1,2, '>'))

  def test_puzzle_guard_turns_right_from_going_right(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".....
.#...
...#.
.....
>...#
""")

    for i in range(4):
      puzzle.move_guard()
    self.assertEqual(puzzle.guard_location, (3,4, 'v'))

  def test_puzzle_guard_moves_right_until_obstacle(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".....
.#...
...#.
.....
>...#
""")
    self.assertEqual(puzzle.guard_location, (0,4, '>'))
    for i in range(3):
      puzzle.move_guard()
    self.assertEqual(puzzle.guard_location, (3,4, '>'))

  def test_puzzle_guard_leaves_map(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".....
.#...
..>#.
.....
....#
""")
    for i in range(3):
      puzzle.move_guard()
    self.assertEqual(puzzle.guard_location, (2,4, 'v'))
    puzzle.move_guard()
    self.assertEqual(puzzle.guard_location, None)

  def test_puzzle_detect_guard_will_leave(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".....
.#...
..>#.
.....
....#
""")
    self.assertEqual(puzzle.guard_will_leave(), True)
    self.assertEqual(puzzle.guard_location, (2,2, '>'))

  def test_puzzle_detect_guard_will_loop(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".....
.#...
..>#.
#....
..#.#
""")
    self.assertEqual(puzzle.guard_will_leave(), False)

if __name__ == '__main__':
    unittest.main(verbosity=2)

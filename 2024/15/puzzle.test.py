import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_map(self):
    puzzle = puz.Puzzle()
    puzzle.process("""########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv
<v>>v<<<
""")

    self.assertEqual(puzzle.width, 8)
    self.assertEqual(puzzle.height, 8)

    self.assertIn((4,4), puzzle.boxes)
    self.assertIn((3,1), puzzle.boxes)
    self.assertEqual(len(puzzle.boxes), 6)

    self.assertIn((0,0), puzzle.walls)
    self.assertIn((2,4), puzzle.walls)

    self.assertEqual(puzzle.robot, (2, 2))

  def test_puzzle_parses_instructions(self):
    puzzle = puz.Puzzle()
    puzzle.process("""########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv
<v>>v<<<
""")

    orders = puzzle.orders
    
    self.assertEqual(orders[0], '<')
    self.assertEqual(orders[7], 'v')
    self.assertEqual(orders[8], '<')
    self.assertEqual(orders[15], '<')

  def test_puzzle_robot_follows_orders(self):
    puzzle = puz.Puzzle()
    puzzle.process("""########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

>v<^>>vv
<v>>v<<<
""")
    
    puzzle.move_robot()
    self.assertEqual(puzzle.robot, (3,2))

    puzzle.move_robot()
    self.assertEqual(puzzle.robot, (3,3))

    puzzle.move_robot()
    self.assertEqual(puzzle.robot, (2,3))

    puzzle.move_robot()
    self.assertEqual(puzzle.robot, (2,2))

  def test_puzzle_robot_does_not_move_when_pushing_a_wall(self):
    puzzle = puz.Puzzle()
    puzzle.process("""########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<<<<<<<<
<v>>v<<<
""")
    
    for i in range(4):
      puzzle.move_robot()

    self.assertEqual(puzzle.robot, (2,2))

  def test_puzzle_robot_pushes_boxes(self):
    puzzle = puz.Puzzle()
    puzzle.process("""########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

>>>>>>>>
<v>>v<<<
""")
    
    for i in range(2):
      puzzle.move_robot()

    self.assertEqual(puzzle.robot, (4,2))
    self.assertNotIn((4,2), puzzle.boxes)
    self.assertIn((5,2), puzzle.boxes)

  def test_puzzle_robot_pushes_all_boxes(self):
    puzzle = puz.Puzzle()
    puzzle.process("""########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

^>>>>>>>
<v>>v<<<
""")
    
    for i in range(3):
      puzzle.move_robot()

    self.assertEqual(puzzle.robot, (4,1))
    self.assertNotIn((3,1), puzzle.boxes)
    self.assertIn((6,1), puzzle.boxes)

  def test_puzzle_robot_cannot_push_box_into_walls(self):
    puzzle = puz.Puzzle()
    puzzle.process("""########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

>>>>>>>>
<v>>v<<<
""")
    
    for i in range(7):
      puzzle.move_robot()

    self.assertEqual(puzzle.robot, (5,2))
    self.assertNotIn((2,4), puzzle.boxes)
    self.assertIn((6,2), puzzle.boxes)

  def test_puzzle_scales_map(self):
    puzzle = puz.Puzzle()
    puzzle.process("""########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv
<v>>v<<<
""")

    puzzle.scale()

    self.assertEqual(puzzle.width, 16)
    self.assertEqual(puzzle.height, 8)

    self.assertIn((8,4), puzzle.boxes)
    self.assertIn((6,1), puzzle.boxes)
    self.assertEqual(len(puzzle.boxes), 6)

    self.assertIn((0,0), puzzle.walls)
    self.assertIn((4,4), puzzle.walls)

    self.assertEqual(puzzle.robot, (4, 2))

  def test_puzzle_robot_pushes_scaled_boxes_together(self):
    puzzle = puz.Puzzle()
    puzzle.process("""########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

^>>>>>vv
<v>>v<<<
""")
    
    puzzle.scale()

    for i in range(6):
      puzzle.move_robot()

    self.assertEqual(puzzle.robot, (9,1))
    self.assertIn((10,1), puzzle.boxes)
    self.assertIn((12,1), puzzle.boxes)

  def test_puzzle_robot_pushes_scaled_boxes_left(self):
    puzzle = puz.Puzzle()
    puzzle.process("""########
#..O.O@#
##..O..#
#..OO..#
#.#.O..#
#...O..#
#......#
########

<<<vvvvv
<v>>v<<<
""")
    
    puzzle.scale()

    for i in range(3):
      puzzle.move_robot()

    self.assertEqual(puzzle.robot, (12-3,1))

    self.assertIn((5,1), puzzle.boxes)
    self.assertIn((7,1), puzzle.boxes)


  def test_puzzle_robot_pushes_scaled_boxes_down(self):
    puzzle = puz.Puzzle()
    puzzle.process("""########
#......#
#......#
#.@O...#
#..OO..#
#......#
#......#
########

>>^>v
""")
    
    puzzle.scale()

    self.assertIn((6,3), puzzle.boxes)
    self.assertIn((6,4), puzzle.boxes)
    self.assertIn((8,4), puzzle.boxes)

    puzzle.move_robot()
    puzzle.move_robot()

    self.assertIn((7,3), puzzle.boxes)
    self.assertIn((6,4), puzzle.boxes)
    self.assertIn((8,4), puzzle.boxes)

    puzzle.move_robot()
    puzzle.move_robot()
    puzzle.move_robot()

    self.assertIn((7,4), puzzle.boxes)
    self.assertIn((6,5), puzzle.boxes)
    self.assertIn((8,5), puzzle.boxes)

  def test_puzzle_robot_cannot_push_if_one_side_blocked(self):
    puzzle = puz.Puzzle()
    puzzle.process("""########
#......#
#......#
#.@O...#
#..OO..#
#...#..#
#......#
########

>>^>v
""")
    
    puzzle.scale()

    self.assertIn((6,3), puzzle.boxes)
    self.assertIn((6,4), puzzle.boxes)
    self.assertIn((8,4), puzzle.boxes)

    puzzle.move_robot()
    puzzle.move_robot()

    self.assertIn((7,3), puzzle.boxes)
    self.assertIn((6,4), puzzle.boxes)
    self.assertIn((8,4), puzzle.boxes)

    puzzle.move_robot()
    puzzle.move_robot()
    puzzle.move_robot()

    self.assertIn((7,3), puzzle.boxes)
    self.assertIn((6,4), puzzle.boxes)
    self.assertIn((8,4), puzzle.boxes)

  def test_puzzle_robot_pushes_scaled_boxes_up(self):
    puzzle = puz.Puzzle()
    puzzle.process("""########
#......#
#......#
#.@OO..#
#..O...#
#......#
#......#
########

v>>v>^
""")
    
    puzzle.scale()

    self.assertIn((6,3), puzzle.boxes)
    self.assertIn((8,3), puzzle.boxes)
    self.assertIn((6,4), puzzle.boxes)

    puzzle.move_robot()
    puzzle.move_robot()
    puzzle.move_robot()

    self.assertIn((6,3), puzzle.boxes)
    self.assertIn((8,3), puzzle.boxes)
    self.assertIn((7,4), puzzle.boxes)

    puzzle.move_robot()
    puzzle.move_robot()
    puzzle.move_robot()

    self.assertIn((6,2), puzzle.boxes)
    self.assertIn((8,2), puzzle.boxes)
    self.assertIn((7,3), puzzle.boxes)


  def test_puzzle_robot_cannot_push_up_if_one_side_blocked(self):
    puzzle = puz.Puzzle()
    puzzle.process("""########
#......#
#..#...#
#.@OO..#
#..O...#
#......#
#......#
########

v>>v>^
""")
    puzzle.scale()

    self.assertIn((6,3), puzzle.boxes)
    self.assertIn((8,3), puzzle.boxes)
    self.assertIn((6,4), puzzle.boxes)

    puzzle.move_robot()
    puzzle.move_robot()
    puzzle.move_robot()

    self.assertIn((6,3), puzzle.boxes)
    self.assertIn((8,3), puzzle.boxes)
    self.assertIn((7,4), puzzle.boxes)

    puzzle.move_robot()
    puzzle.move_robot()
    puzzle.move_robot()

    self.assertIn((6,3), puzzle.boxes)
    self.assertIn((8,3), puzzle.boxes)
    self.assertIn((7,4), puzzle.boxes)

  def test_puzzle_robot_should_not_act_like_box_size_bug(self):
    puzzle = puz.Puzzle()
    puzzle.process("""########
#......#
#......#
#..O...#
#..O...#
#.@O...#
#......#
########

>>^
""")
    puzzle.scale()

    self.assertIn((6,3), puzzle.boxes)
    self.assertIn((6,4), puzzle.boxes)
    self.assertIn((6,5), puzzle.boxes)

    puzzle.move_robot()
    puzzle.move_robot()

    self.assertIn((6,3), puzzle.boxes)
    self.assertIn((6,4), puzzle.boxes)
    self.assertIn((7,5), puzzle.boxes)

    puzzle.dump_map()

    puzzle.move_robot()

    puzzle.dump_map()

    self.assertIn((6,2), puzzle.boxes)
    self.assertIn((6,3), puzzle.boxes)
    self.assertIn((7,5), puzzle.boxes)
    
if __name__ == '__main__':
    unittest.main(verbosity=2)

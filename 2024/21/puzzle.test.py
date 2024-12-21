import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  """
  789
  456
  123
   0A
  """
  def test_puzzle_knows_shortest_paths_for_door_keypad(self):
    puzzle = puz.Puzzle()

    
    paths = puzzle.door_path('A', '9')
    self.assertIn("^^^", paths)
    self.assertEqual(len(paths), 1)

    paths = puzzle.door_path('4', '9')
    self.assertIn("^>>", paths)
    self.assertIn(">>^", paths)
    self.assertIn(">^>", paths)
    self.assertEqual(len(paths), 3)

    paths = puzzle.door_path('0', '7')
    self.assertIn("^^^<", paths)
    self.assertIn("^<^^", paths)
    self.assertIn("^^<^", paths)
    self.assertEqual(len(paths), 3)

  """
   ^A
  <v>
  """
  def test_puzzle_knows_shortest_paths_for_robot_keypad(self):
    puzzle = puz.Puzzle()

    
    paths = puzzle.robot_path('A', 'v')
    self.assertIn("<v", paths)
    self.assertIn("v<", paths)
    self.assertEqual(len(paths), 2)

    paths = puzzle.robot_path('<', 'A')
    self.assertIn(">>^", paths)
    self.assertIn(">^>", paths)
    self.assertEqual(len(paths), 2)

  def test_puzzle_calculates_recursive_presses_to_keyad(self):
    example = "029A"
    expected = "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A"

    puzzle = puz.Puzzle()
    generated = puzzle.generate_keypad_press(example)

    self.assertEqual(len(generated), len(expected))

if __name__ == '__main__':
    unittest.main(verbosity=2)

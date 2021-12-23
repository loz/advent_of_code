import unittest
import puzzle as puz

EXAMPLE="""#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""

class TestPuzzle(unittest.TestCase):

  def test_puzzle_locates_pods(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)

    pods = puzzle.pods
    self.assertEqual(len(pods), 8)
    self.assertTrue(('A',3,3) in pods)
    self.assertTrue(('A',9,3) in pods)
    self.assertTrue(('C',7,3) in pods)
    self.assertTrue(('D',9,2) in pods)

  def test_pod_wont_move_from_right_spot(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)
    
    moves = puzzle.gen_moves(('A',3,3), puzzle.pods)
    self.assertEqual(moves, [])

  def test_pod_wont_move_outside_a_room(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)
    
    moves = puzzle.gen_moves(('B',3,2), puzzle.pods)
    self.assertEqual(len(moves), 7)

  def test_pod_wont_move_to_its_room_of_occupied_by_wrong(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)
    
    moves = puzzle.gen_moves(('B',1,1), [('C',5,3)])
    self.assertEqual(len(moves), 0)

  def test_pod_will_move_to_correct_empty_room(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)
    
    moves = puzzle.gen_moves(('B',1,1), [('C',7,3)])
    self.assertEqual(len(moves), 1)

  def test_pod_will_move_to_room_with_partner(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)
    
    moves = puzzle.gen_moves(('B',1,1), [('B',5,3)])
    self.assertEqual(len(moves), 1)


  def test_pods_in_right_room_will_not_move(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)
    
    moves = puzzle.gen_moves(('B',5,2), [('B',5,2),('B',5,3)])
    self.assertEqual(len(moves), 0)

  def test_pod_under_pod_will_not_move(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)
    
    moves = puzzle.gen_moves(('D',5,3), puzzle.pods)
    self.assertEqual(len(moves), 0)

  def test_pod_along_in_wrong_room_will_move(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)
    
    moves = puzzle.gen_moves(('C',5,3), [('C',5,3), ('B',7,3)])
    self.assertEqual(len(moves), 13)

  #I think this is optimal based on rules!
  #def test_pod_in_room_will_move_straigt_to_right_room(self):
  #  puzzle = puz.Puzzle()
  #  puzzle.process(EXAMPLE)
  #  
  #  moves = puzzle.gen_moves(('C',5,3), [('C',5,3), ('B',9,3)])
  #  self.assertEqual(len(moves), 1)

if __name__ == '__main__':
    unittest.main()

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
    self.assertEqual(len(moves), 9)

  #a pod cannot move to a space through a blocked corridor
  def test_pod_cant_move_through_blocked(self):
    puzzle = puz.Puzzle()
    puzzle.process("""#############
#...C...B...#
###B#.#.#D###
  #A#D#C#A#
  #########
""")
    
    moves = puzzle.gen_moves(('D',5,3), puzzle.pods)
    self.assertEqual(len(moves), 1)

  #a pod will not move to top of empty room
  def test_wont_move_to_top_of_empty_room(self):
    puzzle = puz.Puzzle()
    puzzle.process("""#############
#...C...B...#
###B#C#.#D###
  #A#D#.#A#
  #########
""")
    
    moves = puzzle.gen_moves(('C',4,1), puzzle.pods)
    self.assertEqual(len(moves), 1)

    moves = puzzle.gen_moves(('C',5,2), puzzle.pods)
    #print 'Moves', moves
    #[(6, 1), (7, 2), (7, 3)]
    self.assertEqual(len(moves), 2) #Maybe 1 if skip pointless

  #I think this is optimal based on rules!
  #def test_pod_in_room_will_move_straigt_to_right_room(self):
  #  puzzle = puz.Puzzle()
  #  puzzle.process(EXAMPLE)
  #  
  #  moves = puzzle.gen_moves(('C',5,3), [('C',5,3), ('B',9,3)])
  #  self.assertEqual(len(moves), 1)
 
  def test_cost_calculates_correctly(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)
    #COSTS: a:1, b:10, c:100, D:1000
    self.assertEqual(puzzle.cost(('B',3,3), (1,1)), 4 * 10)
    self.assertEqual(puzzle.cost(('A',3,3), (11,1)), 10)
    self.assertEqual(puzzle.cost(('C',3,3), (5,3)), 6 * 100)
    self.assertEqual(puzzle.cost(('D',1,1), (9,2)), 9 * 1000)


if __name__ == '__main__':
    unittest.main()

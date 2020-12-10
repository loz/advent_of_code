import unittest
import puzzle as puz
import copy

INPUT = (0,[
['thg', 'thc', 'plg', 'stg',],
['plc', 'stc',],
['prg', 'prc', 'rug', 'ruc'],
[]
])

class TestPuzzle(unittest.TestCase):

  def test_state_hash_favours_4floor(self):
    puzzle = puz.Puzzle()
    state1 = copy.deepcopy(INPUT)
    state2 = copy.deepcopy(INPUT)
    e, state = state2
    state[3] = state[0]
    state[0] = []
    hash1 = puzzle.state_hash(state1)
    hash2 = puzzle.state_hash(state2)
    self.assertNotEqual(hash1, hash2)

  def test_state_hash_equiv_floors(self):
    puzzle = puz.Puzzle()
    state1 = copy.deepcopy(INPUT)
    state2 = copy.deepcopy(INPUT)
    e, state = state2
    tmp = state[0]
    state[0] = state[2]
    state[2] = tmp
    hash1 = puzzle.state_hash(state1)
    hash2 = puzzle.state_hash(state2)
    self.assertEqual(hash1, hash2)

  def test_state_hash_equiv_in_floor(self):
    puzzle = puz.Puzzle()
    state1 = copy.deepcopy(INPUT)
    state2 = copy.deepcopy(INPUT)
    e, state = state2
    tmp = state[0]
    first = tmp[0]
    tmp[0] = tmp[2]
    tmp[2] = first
    state[0] = tmp
    hash1 = puzzle.state_hash(state1)
    hash2 = puzzle.state_hash(state2)
    self.assertEqual(hash1, hash2)

  #def test_generate_moves_move_lift_up_2G(self):
  #def test_generate_moves_move_lift_up_1M(self):
  #def test_generate_moves_move_lift_up_2M(self):
  #def test_generate_moves_move_lift_down_1G(self):
  #def test_generate_moves_move_lift_down_2G(self):
  #def test_generate_moves_move_lift_down_1M(self):
  #def test_generate_moves_move_lift_down_2M(self):

  def test_generate_moves_move_lift_up_1G(self):
    puzzle = puz.Puzzle()
    moves = puzzle.generate_moves(INPUT)
    expected = (1,[
['thc', 'plg', 'stg',],
['plc', 'stc', 'thg'],
['prg', 'prc', 'rug', 'ruc'],
[]
])
    found = expected in moves
    self.assertTrue(found)

  def test_generate_moves_move_lift_up_1C(self):
    puzzle = puz.Puzzle()
    moves = puzzle.generate_moves(INPUT)
    expected = (1,[
['thg', 'plg', 'stg',],
['plc', 'stc', 'thc'],
['prg', 'prc', 'rug', 'ruc'],
[]
])
    found = expected in moves
    self.assertTrue(found)

  def test_generate_moves_move_lift_up_2G(self):
    puzzle = puz.Puzzle()
    moves = puzzle.generate_moves(INPUT)
    expected = (1,[
['thc', 'plg'],
['plc', 'stc', 'thg', 'stg'],
['prg', 'prc', 'rug', 'ruc'],
[]
])
    found = expected in moves
    self.assertTrue(found)

  def test_generate_moves_move_lift_up_2C(self):
    puzzle = puz.Puzzle()
    _, state = INPUT
    moves = puzzle.generate_moves((1, state))
    expected = (2,[
['thg', 'thc', 'plg', 'stg'],
[],
['prg', 'prc', 'rug', 'ruc', 'plc', 'stc'],
[]
])
    found = expected in moves
    self.assertTrue(found)

  def test_generate_moves_move_lift_down_2C(self):
    puzzle = puz.Puzzle()
    _, state = INPUT
    moves = puzzle.generate_moves((1, state))
    expected = (0,[
['thg', 'thc', 'plg', 'stg', 'plc', 'stc'],
[],
['prg', 'prc', 'rug', 'ruc'],
[]
])
    found = expected in moves
    self.assertTrue(found)

  def test_valid_state(self):
    puzzle = puz.Puzzle()
    _, state = INPUT
    valid = puzzle.valid_state((1, state))
    self.assertTrue(valid)

  def test_invalid_state(self):
    puzzle = puz.Puzzle()
    state = (0,[
['thg', 'thc', 'stg', 'plc', 'stc'],
[],
['prg', 'prc', 'rug', 'ruc'],
[]
])
    valid = puzzle.valid_state(state)
    self.assertFalse(valid)

if __name__ == '__main__':
    unittest.main()

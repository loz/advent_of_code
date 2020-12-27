import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_swap_position_xy(self):
    puzzle = puz.Puzzle()
    puzzle.process("""swap position 7 with position 1
""")
    result = puzzle.encode('abcdefgh')
    self.assertEqual(result, 'ahcdefgb')

  def test_swap_letters(self):
    puzzle = puz.Puzzle()
    puzzle.process("""swap letter a with letter b
""")
    result = puzzle.encode('abababab')
    self.assertEqual(result, 'babababa')

  def test_rotate_left(self):
    puzzle = puz.Puzzle()
    puzzle.process("""rotate left 3 steps
""")
    result = puzzle.encode('abcdefgh')
    self.assertEqual(result, 'defghabc')

  def test_rotate_right(self):
    puzzle = puz.Puzzle()
    puzzle.process("""rotate right 1 step
""")
    result = puzzle.encode('abcdefgh')
    self.assertEqual(result, 'habcdefg')

  def test_rotate_based_on_letter(self):
    puzzle = puz.Puzzle()
    puzzle.process("""rotate based on position of letter d
""")
    result = puzzle.encode('abcdefgh')
    self.assertEqual(result, 'efghabcd')

  def test_reverse_positions(self):
    puzzle = puz.Puzzle()
    puzzle.process("""reverse positions 3 through 5
""")
    result = puzzle.encode('abcdefgh')
    self.assertEqual(result, 'abcfedgh')

  def test_move_positions(self):
    puzzle = puz.Puzzle()
    puzzle.process("""move position 1 to position 5
move position 3 to position 0
""")
    result = puzzle.encode('abcdefgh')
    self.assertEqual(result, 'eacdfbgh')

  def test_decode_works(self):
    puzzle = puz.Puzzle()
    puzzle.process("""swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d
""")
    result = puzzle.encode('abcdefgh')
    result = puzzle.decode(result)
    self.assertEqual(result, 'abcdefgh')



if __name__ == '__main__':
    unittest.main()

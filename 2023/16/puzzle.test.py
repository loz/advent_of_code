import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_grid(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".|..
.\.|
.-./
""")

    self.assertEqual(puzzle.at(1, 0), '|')
    self.assertEqual(puzzle.at(1, 1), '\\')
    self.assertEqual(puzzle.at(3, 2), '/')

  def test_puzzle_beam_goes_right(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".|..
.\.|
.-./
""")
    
    self.assertEqual(puzzle.beam('r', (0, 0)), [('r', (1, 0))])

  def test_puzzle_beam_reflects_right_down(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".|..
.\.|
.-./
""")
    
    self.assertEqual(puzzle.beam('r', (1, 1)), [('d', (1, 2))])

  def test_puzzle_beam_reflects_right_up(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".|..
.\.|
.-./
""")
    
    self.assertEqual(puzzle.beam('r', (3, 2)), [('u', (3, 1))])

  def test_puzzle_beam_splits_right_up_and_down(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".|..
.\.|
.-./
""")
    
    self.assertEqual(puzzle.beam('r', (3, 1)), [('u', (3, 0)), ('d', (3, 2))])

  def test_puzzle_beam_splits_right_right(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".|..
.\.|
.-./
""")
    
    self.assertEqual(puzzle.beam('r', (1, 2)), [('r', (2, 2))])

  def test_puzzle_beam_goes_left(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".|..
.\.|
.-./
""")
    
    self.assertEqual(puzzle.beam('l', (3, 0)), [('l', (2, 0))])

  def test_puzzle_beam_splits_left_left(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".|..
.\.|
.-./
""")
    
    self.assertEqual(puzzle.beam('l', (1, 2)), [('l', (0, 2))])

  def test_puzzle_beam_reflects_left_up(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".|..
.\.|
.-./
""")
    
    self.assertEqual(puzzle.beam('l', (1, 1)), [('u', (1, 0))])

  def test_puzzle_beam_reflects_left_down(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".|..
.\.|
.-./
""")
    
    self.assertEqual(puzzle.beam('l', (3, 2)), [('d', (3, 3))])

  def test_puzzle_beam_splits_left_up_and_down(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".|..
.\.|
.-./
""")
    
    self.assertEqual(puzzle.beam('l', (3, 1)), [('u', (3, 0)), ('d', (3, 2))])

  def test_puzzle_beam_goes_down(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".|..
.\.|
.-./
""")
    
    self.assertEqual(puzzle.beam('d', (0, 0)), [('d', (0, 1))])

  def test_puzzle_beam_splits_down_down(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".|..
.\.|
.-./
""")
    
    self.assertEqual(puzzle.beam('d', (1, 0)), [('d', (1, 1))])

  def test_puzzle_beam_reflects_down_right(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".|..
.\.|
.-./
""")
    
    self.assertEqual(puzzle.beam('d', (1, 1)), [('r', (2, 1))])

  def test_puzzle_beam_reflects_down_left(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".|..
.\.|
.-./
""")
    
    self.assertEqual(puzzle.beam('d', (3, 2)), [('l', (2, 2))])

  def test_puzzle_beam_splits_down_left_right(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".|..
.\.|
.-./
""")
    
    self.assertEqual(puzzle.beam('d', (1, 2)), [('l', (0, 2)), ('r', (2, 2))])

  def test_puzzle_beam_goes_up(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".|..
.\.|
.-./
""")
    
    self.assertEqual(puzzle.beam('u', (0, 0)), [('u', (0, -1))])

  def test_puzzle_beam_splits_up_up(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".|..
.\.|
.-./
""")
    
    self.assertEqual(puzzle.beam('u', (1, 0)), [('u', (1, -1))])

  def test_puzzle_beam_reflects_up_left(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".|..
.\.|
.-./
""")
    
    self.assertEqual(puzzle.beam('u', (1, 1)), [('l', (0, 1))])

  def test_puzzle_beam_reflects_up_right(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".|..
.\.|
.-./
""")
    
    self.assertEqual(puzzle.beam('u', (3, 2)), [('r', (4, 2))])

  def test_puzzle_beam_splits_up_left_right(self):
    puzzle = puz.Puzzle()
    puzzle.process(""".|..
.\.|
.-./
""")
    
    self.assertEqual(puzzle.beam('u', (1, 2)), [('l', (0, 2)), ('r', (2, 2))])


if __name__ == '__main__':
    unittest.main()

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_gen_paths_start(self):
    puzzle = puz.Puzzle()
    loc = (0,0)
    passcode = "hijkl"
    
    options = puzzle.gen_paths(loc, passcode)
    self.assertEqual(len(options), 1)
    choice = options[0]
    loc, path = choice
    self.assertEqual(loc, (0,1))
    self.assertEqual(path, passcode + 'D')

if __name__ == '__main__':
    unittest.main()

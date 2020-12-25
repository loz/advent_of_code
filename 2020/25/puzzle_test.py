import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_can_find_loop(self):
    puzzle = puz.Puzzle()

    self.assertEqual(puzzle.calcloop(5764801,7),8)
    self.assertEqual(puzzle.calcloop(17807724,7),11)

  def test_can_encode(self):
    puzzle = puz.Puzzle()

    pubkey1 = 5764801
    pubkey2 = 17807724
    encoded = puzzle.encode(pubkey1, 11)
    encoded2 = puzzle.encode(pubkey2, 8)
    
    self.assertEqual(encoded, encoded2)
    self.assertEqual(encoded, 14897079)


if __name__ == '__main__':
    unittest.main()

import unittest
import puzzle as puz

EXAMPLE="""0: 3
1: 2
4: 4
6: 4
"""

class TestPuzzle(unittest.TestCase):

  def test_process_recording(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)

    self.assertEqual(puzzle.depth(0), 3)
    self.assertEqual(puzzle.depth(4), 4)
    self.assertEqual(puzzle.depth(6), 4)

  def test_scanner_inits_at_top(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)

    self.assertEqual(puzzle.scannerAt(0), 0)
    self.assertEqual(puzzle.scannerAt(4), 0)
    self.assertEqual(puzzle.scannerAt(6), 0)

  def test_scanner_moves_with_tick(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)
    puzzle.tick()
    self.assertEqual(puzzle.scannerAt(0), 1)
    self.assertEqual(puzzle.scannerAt(4), 1)
    self.assertEqual(puzzle.scannerAt(6), 1)

  def test_scanner_moves_up_from_bottom(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)
    puzzle.tick()
    puzzle.tick()
    puzzle.tick()
    self.assertEqual(puzzle.scannerAt(0), 1)
    self.assertEqual(puzzle.scannerAt(1), 1)

  def test_packet_starts_outside(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)
    self.assertEqual(puzzle.packet_loc, -1)

  def test_packet_moves_depth_with_tick(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)
    puzzle.tick()
    self.assertEqual(puzzle.packet_loc, 0)
  
  def test_packet_is_caught_when_scanner_present(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)
    for i in range(7):
      puzzle.tick()
    self.assertEqual(puzzle.packet_loc, 6)
    hits = puzzle.hits()
    self.assertTrue(0 in hits)
    self.assertTrue(6 in hits)
    self.assertEqual(puzzle.severity(), 24)

  def test_can_calculate_safe_at_given_delay(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)
    self.assertFalse(puzzle.safe_delay(9))
    self.assertTrue(puzzle.safe_delay(10))
    


if __name__ == '__main__':
    unittest.main()

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_regions_separate(self):
    puzzle = puz.Puzzle()
    puzzle.process("""on x=0..1,y=0..1,z=0..1
on x=2..3,y=2..3,z=2..3
""")
    self.assertEqual(puzzle.count_on(), 16)

  def test_regions_corner_corner_overlap(self):
    puzzle = puz.Puzzle()
    puzzle.process("""on x=0..2,y=0..2,z=0..2
on x=2..3,y=2..3,z=2..3
""")
    self.assertEqual(puzzle.count_on(), 34)

  def test_regions_side_corner_overlap(self):
    puzzle = puz.Puzzle()
    puzzle.process("""on x=0..3,y=0..3,z=0..3
on x=1..2,y=2..4,z=2..4
""")
    self.assertEqual(puzzle.count_on(), 74)

  def test_regions_side_overlap(self):
    puzzle = puz.Puzzle()
    puzzle.process("""on x=0..4,y=0..4,z=0..2
on x=2..3,y=2..3,z=2..3
""")
    self.assertEqual(puzzle.count_on(), 79)

#  def test_regions_consume(self):
#    puzzle = puz.Puzzle()
#    puzzle.process("""on x=2..2,y=2..2,z=2..2
#on x=1..3,y=1..3,z=1..3
#on x=1..2,y=2..2,z=2..2
#""")
#    self.assertEqual(puzzle.count_on(), 27)
#
#  def test_remove_separate(self):
#    puzzle = puz.Puzzle()
#    puzzle.process("""on x=0..1,y=0..1,z=0..1
#off x=2..3,y=2..3,z=2..3
#""")
#    self.assertEqual(puzzle.count_on(), 8)
#
#  def test_remove_corner_overlap(self):
#    puzzle = puz.Puzzle()
#    puzzle.process("""on x=0..2,y=0..2,z=0..2
#off x=2..3,y=2..3,z=2..3
#""")
#    self.assertEqual(puzzle.count_on(), 26)
#
#  def test_remove_side_overlap(self):
#    puzzle = puz.Puzzle()
#    puzzle.process("""on x=0..4,y=0..4,z=0..2
#off x=2..3,y=2..3,z=2..3
#""")
#    self.assertEqual(puzzle.count_on(), 71)
#
#  def test_remove_consume(self):
#    puzzle = puz.Puzzle()
#    puzzle.process("""on x=2..2,y=2..2,z=2..2
#off x=1..3,y=1..3,z=1..3
#on x=1..2,y=2..2,z=2..2
#""")
#    self.assertEqual(puzzle.count_on(), 2)
#
#
#  def test_puzzle_turns_on(self):
#    puzzle = puz.Puzzle()
#    puzzle.process("""on x=2..3,y=0..1,z=2..2
#""")
#    self.assertEqual(puzzle.count_on(), 4)
#    self.assertTrue((2,0,2) in puzzle.on)
#    self.assertTrue((3,1,2) in puzzle.on)
#
#  def test_puzzle_turns_off(self):
#    puzzle = puz.Puzzle()
#    puzzle.process("""on x=0..4,y=0..4,z=0..4
#off x=2..3,y=0..1,z=2..2
#""")
#    self.assertEqual(puzzle.count_on(), 121)
#    self.assertFalse((2,0,2) in puzzle.on)
#    self.assertFalse((3,1,2) in puzzle.on)

  def test_remove_separate(self):
    puzzle = puz.Puzzle()
    puzzle.process("""on x=0..1,y=0..1,z=0..1
off x=2..3,y=2..3,z=2..3
""")
    self.assertEqual(puzzle.count_on(), 8)

  def test_remove_corner_overlap(self):
    puzzle = puz.Puzzle()
    puzzle.process("""on x=0..2,y=0..2,z=0..2
off x=2..3,y=2..3,z=2..3
""")
    self.assertEqual(puzzle.count_on(), 26)

  def test_remove_side_overlap(self):
    puzzle = puz.Puzzle()
    puzzle.process("""on x=0..4,y=0..4,z=0..2
off x=2..3,y=2..3,z=2..3
""")
    self.assertEqual(puzzle.count_on(), 71)

  def test_remove_side_inside(self):
    puzzle = puz.Puzzle()
    puzzle.process("""on x=0..4,y=0..4,z=0..4
off x=1..3,y=1..3,z=1..3
""")
    self.assertEqual(puzzle.count_on(), 5**3 - 3**3)

  def test_remove_consume(self):
    puzzle = puz.Puzzle()
    puzzle.process("""on x=2..2,y=2..2,z=2..2
off x=1..3,y=1..3,z=1..3
on x=1..2,y=2..2,z=2..2
""")
    self.assertEqual(puzzle.count_on(), 2)

  def test_bug1(self):
    print '====== BUG ========'
    puzzle = puz.Puzzle()
    puzzle.process("""on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
""")
    self.assertEqual(puzzle.count_on(), 32)

if __name__ == '__main__':
    unittest.main()

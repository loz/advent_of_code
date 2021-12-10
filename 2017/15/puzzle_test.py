import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle(self):
    puzzle = puz.Puzzle()
    puzzle.process("""inputhere
""")
    pass

  def test_generates_a(self):
    puzzle = puz.Puzzle()
    puzzle.process("""inputhere
""")
    self.assertEqual(puzzle.generateA(1092455), 1181022009) 

  def test_generates_b(self):
    puzzle = puz.Puzzle()
    puzzle.process("""inputhere
""")
    self.assertEqual(puzzle.generateB(430625591), 1233683848) 

  def test_generates_a2(self):
    puzzle = puz.Puzzle()
    puzzle.process("""inputhere
""")
    self.assertEqual(puzzle.generateA2(1352636452), 1992081072) 

  def test_generates_b2(self):
    puzzle = puz.Puzzle()
    puzzle.process("""inputhere
""")
    self.assertEqual(puzzle.generateB2(1233683848), 862516352) 

  def test_judge_does_not_match(self):
    puzzle = puz.Puzzle()
    puzzle.process("""inputhere
""")
    self.assertFalse(puzzle.judge(1181022009, 1233683848))

  def test_judge_does_match(self):
    puzzle = puz.Puzzle()
    puzzle.process("""inputhere
""")
    self.assertTrue(puzzle.judge(245556042, 1431495498))

if __name__ == '__main__':
    unittest.main()

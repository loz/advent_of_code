import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_columns(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1 23 560
2 22 653
3 1 234
+ * +
""")
  
    problems = puzzle.problems
    self.assertEqual(len(problems), 3)

    self.assertIn(([1, 2, 3],'+'), problems)
    self.assertIn(([23, 22, 1],'*'), problems)
    self.assertIn(([560, 653, 234],'+'), problems)

  def test_puzzle_eval_problem(self):
    puzzle = puz.Puzzle()

    self.assertEqual(puzzle.eval_problem(([1,2,3],'+')), 6)
    self.assertEqual(puzzle.eval_problem(([23,22,1],'*')), 23*22)

  def test_puzzle_map_cephalapod_numbers(self):
    puzzle = puz.Puzzle()
    puzzle.process2("""
12 23 560
 2 22 653
 3  1 234
+  *  +  
""")
  
    problems = puzzle.problems
    self.assertEqual(len(problems), 3)

    self.assertIn(([1, 223],'+'), problems)
    self.assertIn(([22, 321],'*'), problems)
    self.assertIn(([562, 653, 34],'+'), problems)


if __name__ == '__main__':
    unittest.main(verbosity=2)

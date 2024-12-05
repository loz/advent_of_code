import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_rules(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1|2
3|4
5|6

1,2,3,4
""")
    self.assertEqual(puzzle.rules[0], (1,2))
    self.assertEqual(puzzle.rules[1], (3,4))
    self.assertEqual(puzzle.rules[2], (5,6))

  def test_puzzle_parses_orders(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1|2
3|4
5|6

1,2,3,4
""")
    self.assertEqual(puzzle.orders[0], [1,2,3,4])

  def test_puzzle_order_valid_with_1_item(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1|2
3|4
5|6

1,2,3,4
""")

    self.assertEqual(puzzle.valid_order([1]), True)

  def test_puzzle_order_not_valid_with_later_item_early(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1|2
3|4
5|6

1,2,3,4
""")

    self.assertEqual(puzzle.valid_order([4,1,3]), False)

  def test_puzzle_order_valid_if_dependency_not_needed(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1|2
3|4
5|6

1,2,3,4
""")

    self.assertEqual(puzzle.valid_order([1,4]), True)

  def test_puzzle_fixes_order(self):
    puzzle = puz.Puzzle()
    puzzle.process("""1|2
3|4
5|6

1,2,3,4
""")

    self.assertEqual(puzzle.sort_order([4,1,3]), [3,1,4])
    #self.assertEqual(puzzle.sort_order([4,1,3]), [1,3,4])

if __name__ == '__main__':
    unittest.main()

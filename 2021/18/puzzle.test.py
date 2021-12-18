import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_fish_number(self):
    puzzle = puz.Puzzle()
    puzzle.process("""[[[[1,2],[3,4]],[[5,6],[7,8]]],9]
""")
    number = puzzle.numbers[0]
    self.assertEqual(number.right.val, 9)
    self.assertEqual(number.left.left.left.left.val, 1)

  def test_puzzle_fish_reduces_explode(self):
    puzzle = puz.Puzzle()
    puzzle.process("""[[[[[9,8],1],2],3],4]
[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]
""")
    number = puzzle.numbers[0]
    number.reduce()
    #[[[[0,9],2],3],4]
    self.assertEqual(number.right.val, 4)
    self.assertEqual(number.left.left.left.left.val, 0)

    number = puzzle.numbers[1]
    number.reduce()
    #[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
    self.assertEqual(number.right.left.val, 9)
    self.assertEqual(number.left.right.right.left.val, 8)





if __name__ == '__main__':
    unittest.main()

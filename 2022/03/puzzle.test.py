import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_bags_split_evenly(self):
    puzzle = puz.Puzzle()
    puzzle.process("""abCdEfgh
""")
    bag = puzzle.bags[0]
    left, right = bag
    self.assertEquals(left, ['a', 'b', 'C', 'd'])
    self.assertEquals(right, ['E', 'f', 'g', 'h'])

  def test_puzzle_finds_shared(self):
    puzzle = puz.Puzzle()
    puzzle.process("""abCdEfag
""")
    bag = puzzle.bags[0]
    shared = puzzle.shared(bag)

    self.assertEquals(shared, ['a'])

  def test_puzzle_groups_elves(self):
    puzzle = puz.Puzzle()
    puzzle.process("""abcafg
awewst
alnrlt
zqwwer
poziuy
lnikzl
""")
    group = puzzle.group(0)
    bag = group[1]
    self.assertEquals(bag, (['a', 'w', 'e'], ['w', 's', 't']))

    group = puzzle.group(1)
    bag = group[0]
    self.assertEquals(bag, (['z', 'q', 'w'], ['w', 'e', 'r']))

  def test_puzzle_identifies_badge(self):
    puzzle = puz.Puzzle()
    puzzle.process("""abcafg
awewst
alnrlt
zqwwer
poziuy
lnikzl
""")
    group = puzzle.group(0)
    self.assertEquals(puzzle.badge(group), 'a')

    group = puzzle.group(1)
    self.assertEquals(puzzle.badge(group), 'z')

  def test_puzzle_counts_priority(self):
    puzzle = puz.Puzzle()
    items = ['p', 'L', 'P', 'v', 't', 's']

    self.assertEquals(puzzle.priority(items), 157)


if __name__ == '__main__':
    unittest.main()

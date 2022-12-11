import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_notes(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Monkey 0:
  Starting items: 2, 9
  Operation: new = old * 20
  Test: divisible by 21
    If true: throw to monkey 10
    If false: throw to monkey 3
""")

    monkey = puzzle.monkeys[0]
    self.assertEquals(monkey.items, [2, 9])
    self.assertEquals(monkey.operation, ('old', '*', 20))
    self.assertEquals(monkey.divisor, 21)
    self.assertEquals(monkey.targets, (10, 3))
    self.assertEquals(monkey.id, 0)

  def test_monkey_plays(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Monkey 0:
  Starting items: 1, 2
  Operation: new = old * 3
  Test: divisible by 2
    If true: throw to monkey 0
    If false: throw to monkey 1

Monkey 1:
  Starting items: 3, 10
  Operation: new = old + old
  Test: divisible by 3
    If true: throw to monkey 1
    If false: throw to monkey 0
""")

    monkey1 = puzzle.monkeys[0]
    monkey2 = puzzle.monkeys[1]

    monkey1.play(puzzle.monkeys)

    #1*3 = 3 / 3 = 1 is odd => 1
    #2*3 = 3 / 3 = 2 is even => 0
    self.assertEquals(monkey2.items, [3, 10, 1])

    monkey2.play(puzzle.monkeys)
    #3+3 = 6 / 3 = 2 is not/3 => 1
    #10+10 = 20 / 3 = 6 is /3 => 0
    #1+1 = 2 / 3 = 0 is is /3 => 0
    self.assertEquals(monkey1.items, [2])


    

if __name__ == '__main__':
    unittest.main()

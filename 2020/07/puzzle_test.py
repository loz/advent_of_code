import unittest
import puzzle as puz

INPUT="""light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
"""

class TestPuzzle(unittest.TestCase):

  def test_parses_links(self):
    puzzle = puz.Puzzle()
    puzzle.process(INPUT)
    links = puzzle.links['faded blue']
    self.assertEqual(links[0], (0, 'other'))
    links = puzzle.links['light red']
    self.assertEqual(links[0], (1, 'bright white'))
    self.assertEqual(links[1], (2, 'muted yellow'))

  def test_eventually_contains(self):
    puzzle = puz.Puzzle()
    puzzle.process(INPUT)
    self.assertFalse(puzzle.eventually_contains('shiny gold', 'faded blue'))
    self.assertTrue(puzzle.eventually_contains('shiny gold', 'bright white'))
    self.assertFalse(puzzle.eventually_contains('light red', 'dark olive'))
    self.assertTrue(puzzle.eventually_contains('faded blue', 'dark orange'))

  def test_count_contiains(self):
    puzzle = puz.Puzzle()
    puzzle.process(INPUT)
    self.assertEqual(puzzle.count_contains('faded blue'), 0 + 1)
    self.assertEqual(puzzle.count_contains('dark olive'), 7 + 1)
    self.assertEqual(puzzle.count_contains('shiny gold'), 32 + 1)
    

if __name__ == '__main__':
    unittest.main()

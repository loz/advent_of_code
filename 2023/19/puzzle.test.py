import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_rules(self):
    puzzle = puz.Puzzle()
    puzzle.process("""abc{x>10:cde,m<5:efg,a>3:R,A}
cde{x<5:R,m>5:A,a>3:R,A}

{x=10, m=20, a=30, s=40}
{x=3, m=6, a=9, s=12}
""")
    self.assertEqual(puzzle.rules['abc'], [('x', '>', 10, 'cde'), ('m', '<', 5, 'efg'), ('a', '>', 3, 'R'), (None, 'A')])

  def test_puzzle_parses_parts(self):
    puzzle = puz.Puzzle()
    puzzle.process("""abc{x>10:cde,m<5:efg,a>3:R,A}
cde{x<5:R,m>5:A,a>3:R,A}

{x=10,m=20,a=30,s=40}
{x=3,m=6,a=9,s=12}
""")
    self.assertEqual(puzzle.parts[0], {'x':10, 'm':20, 'a':30, 's':40})

  def test_puzzle_matches_on_first_step(self):
    puzzle = puz.Puzzle()
    puzzle.process("""abc{x>10:cde,m<5:efg,a>3:R,A}
cde{x<5:R,m>5:A,a>3:R,A}

{x=10,m=20,a=30,s=40}
{x=3,m=6,a=9,s=12}
""")
    self.assertEqual(puzzle.match('abc', {'x':11}), 'cde')

  def test_puzzle_matches_on_second_step(self):
    puzzle = puz.Puzzle()
    puzzle.process("""abc{x>10:cde,m<5:efg,a>3:R,A}
cde{x<5:R,m>5:A,a>3:R,A}

{x=10,m=20,a=30,s=40}
{x=3,m=6,a=9,s=12}
""")
    self.assertEqual(puzzle.match('abc', {'x':10, 'm':4}), 'efg')

  def test_puzzle_matches_on_last_step(self):
    puzzle = puz.Puzzle()
    puzzle.process("""abc{x>10:cde,m<5:efg,a>3:R,A}
cde{x<5:R,m>5:A,a>3:R,A}

{x=10,m=20,a=30,s=40}
{x=3,m=6,a=9,s=12}
""")
    self.assertEqual(puzzle.match('abc', {'x':10, 'm':5, 'a':3}), 'A')


  def test_puzzle_range_maps(self):
    puzzle = puz.Puzzle()
    puzzle.process("""abc{x>10:cde,m<5:efg,a>3:R,A}
cde{x<5:R,m>5:A,a>3:R,A}

{x=10,m=20,a=30,s=40}
{x=3,m=6,a=9,s=12}
""")
    ranges = {'x':(1,1000), 'm':(1,1000), 'a':(1,1000), 's':(1,1000)}
    nexts = puzzle.range_map('abc', ranges)
    self.assertEqual(('cde', {'x':(11,1000), 'm':(1,1000), 'a':(1,1000), 's':(1,1000)}) in nexts)
    self.assertEqual(('efg', {'x':(1,10), 'm':(1,4), 'a':(1,1000), 's':(1,1000)}) in nexts)
    self.assertEqual(('R', {'x':(1,10), 'm':(5,1000), 'a':(4,1000), 's':(1,1000)}) in nexts)
    self.assertEqual(('A', {'x':(1,10), 'm':(5,1000), 'a':(1,3), 's':(1,1000)}) in nexts)

if __name__ == '__main__':
    unittest.main()

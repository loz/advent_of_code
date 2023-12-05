import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_seeds(self):
    puzzle = puz.Puzzle()
    puzzle.process("""seeds: 1 23 45 67

seed-to-soil map:
10 20 30

foo-to-bar map:
12 34 56

bar-to-baz map:
11 22 33
44 55 66
""")
    self.assertEqual(puzzle.seeds, [1, 23, 45, 67])

  def test_puzzle_parses_maps(self):
    puzzle = puz.Puzzle()
    puzzle.process("""seeds: 1 23 45 67

seed-to-soil map:
10 20 30

foo-to-bar map:
12 34 56

bar-to-baz map:
11 22 33
44 55 66
""")

    
    self.assertEqual(puzzle.maps['seed'], ('soil', [[10, 20, 30]]))
    self.assertEqual(puzzle.maps['foo'], ('bar', [[12, 34, 56]]))
    self.assertEqual(puzzle.maps['bar'], ('baz', [[11, 22, 33], [44, 55, 66]]))

  def test_puzzle_mapping_number_out_range_to_self(self):
    puzzle = puz.Puzzle()
    puzzle.process("""seeds: 1 23 45 67

foo-to-bar map:
12 34 56

bar-to-baz map:
11 22 33
44 55 66
""")

    
    self.assertEqual(puzzle.map('foo', 10), ('bar', 10))

  def test_puzzle_mapping_start_range_to_start_dst_range(self):
    puzzle = puz.Puzzle()
    puzzle.process("""seeds: 1 23 45 67

foo-to-bar map:
12 34 56

bar-to-baz map:
11 22 33
54 55 66
""")

    
    self.assertEqual(puzzle.map('foo', 34), ('bar', 12))
    self.assertEqual(puzzle.map('bar', 55), ('baz', 54))

  def test_puzzle_mapping_within_range(self):
    puzzle = puz.Puzzle()
    puzzle.process("""seeds: 1 23 45 67

foo-to-bar map:
12 34 56

bar-to-baz map:
11 22 33
54 55 66
""")

    
    self.assertEqual(puzzle.map('bar', 30), ('baz', 19))


  def test_puzzle_rangemapping_maps_start_and_end(self):
    puzzle = puz.Puzzle()
    puzzle.process("""seeds: 1 23 45 67

foo-to-bar map:
12 34 56

bar-to-baz map:
11 22 33
54 55 66
""")

    
    self.assertEqual(puzzle.range_map('bar', 30, 40), ('baz', [(19,29)]))

  def test_puzzle_rangemapping_maps_sets_of_range_outside(self):
    puzzle = puz.Puzzle()
    puzzle.process("""seeds: 1 23 45 67

foo-to-bar map:
12 34 56

bar-to-baz map:
54 55 66
11 22 33
""")

    
    self.assertEqual(puzzle.range_map('foo', 1, 100), ('bar', [(1,33), (12,67), (90,100)]))


  def test_puzzle_rangemapping_maps_bug1(self):
    puzzle = puz.Puzzle()
    puzzle.process("""seeds: 1 23 45 67

water-to-light map:
88 18 7
18 25 70
""")
    self.assertEqual(puzzle.range_map('water', 81, 94), ('light', [(74,87)]))

  def test_puzzle_rangemapping_maps_bug2(self):
    puzzle = puz.Puzzle()
    puzzle.process("""seeds: 1 23 45 67

light-to-temperature map:
45 77 23
81 45 19
68 64 13
""")
    self.assertEqual(puzzle.range_map('light', 74, 87), ('temperature', [(78,80), (45,55)]))

if __name__ == '__main__':
    unittest.main()

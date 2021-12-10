import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle(self):
    puzzle = puz.Puzzle()
    puzzle.process("""flqrgnkx
""")
    pass

  def test_puzzle_encodes_hash(self):
    puzzle = puz.Puzzle()
    frag_str = puzzle.frag_string('a0c2017')
    self.assertEqual(frag_str, '#.#.....##....#........#.###')

  def test_puzzle_counts_regions(self):
    puzzle = puz.Puzzle()
    count = puzzle.count_regions([
      '#...#...',
      '##...###',
      '###....#',
      '...####.',
      '#..##...',
      '##.##..#'
    ])
    self.assertEqual(count, 6)

if __name__ == '__main__':
    unittest.main()

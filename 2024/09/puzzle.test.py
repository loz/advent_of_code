import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_diskmap(self):
    puzzle = puz.Puzzle()
    puzzle.process("""12345
""")
    self.assertEqual(puzzle.diskmap, [1, 2, 3, 4, 5])

  def test_puzzle_decompresses_diskmap(self):
    puzzle = puz.Puzzle()

    blocks = puzzle.decompress([1, 2, 3, 4, 5])

    self.assertEqual(blocks, [(0, 1), (None, 2), (1, 3), (None, 4), (2, 5)])

  def test_puzzle_decompresses_zero_sized_blocks_ignored(self):
    puzzle = puz.Puzzle()

    blocks = puzzle.decompress([1, 0, 3, 0, 0])

    self.assertEqual(blocks, [(0, 1), (1, 3)])

  def test_puzzle_defrags_single_block(self):
    puzzle = puz.Puzzle()

    blocks = puzzle.decompress([1, 2, 3, 4, 5])
    did, blocks = puzzle.defrag(blocks)
    self.assertTrue(did)
    self.assertEqual(blocks, [(0, 1), (2, 1), (None, 1), (1, 3), (None, 4), (2, 4), (None, 1)])

  def test_puzzle_defrags_removes_empty_gaps(self):
    puzzle = puz.Puzzle()

    blocks = puzzle.decompress([1, 2, 3, 4, 5])
    did, blocks = puzzle.defrag(blocks)
    did, blocks = puzzle.defrag(blocks)
    self.assertTrue(did)
    self.assertEqual(blocks, [(0, 1), (2, 2), (1, 3), (None, 4), (2, 3), (None, 2)])

  def test_puzzle_defrags_removes_empty_chunks(self):
    puzzle = puz.Puzzle()

    blocks = puzzle.decompress([1, 2, 3, 4, 5])
    for i in range(5):
      did, blocks = puzzle.defrag(blocks)

    self.assertEqual(blocks, [(0, 1), (2, 2), (1, 3), (2, 3), (None, 6)])

  def test_puzzle_did_not_defrag_when_no_defrag(self):
    puzzle = puz.Puzzle()

    blocks = puzzle.decompress([1, 2, 3, 4, 5])
    for i in range(5):
      did, blocks = puzzle.defrag(blocks)

    did, blocks = puzzle.defrag(blocks)
    self.assertEqual(did, False)

  def test_puzzle_calculates_checksum(self):
    puzzle = puz.Puzzle()

    blocks = puzzle.decompress([1, 2, 3, 4, 5])
    for i in range(5):
      did, blocks = puzzle.defrag(blocks)

    checksum = puzzle.checksum(blocks)
    self.assertEqual(checksum, 1*2 + 2*2 + 3 + 4 + 5 + 6*2 + 7*2 + 8*2)

  def test_puzzle_super_defrag_moves_whole_files(self):
    puzzle = puz.Puzzle()

    blocks = [(0, 1), (None, 5), (1, 2), (None, 3), (2, 2)]
    blocks = puzzle.super_defrag(blocks)

    self.assertEqual(blocks, [(0, 1), (2, 2), (1, 2), (None, 8)])

  def test_puzzle_super_defrag_file_whole_gaps(self):
    puzzle = puz.Puzzle()

    blocks = [(0, 1), (None, 5), (1, 2), (None, 3), (2, 5)]
    blocks = puzzle.super_defrag(blocks)

    self.assertEqual(blocks, [(0, 1), (2, 5), (1, 2), (None, 8)])
    

if __name__ == '__main__':
    unittest.main(verbosity=2)

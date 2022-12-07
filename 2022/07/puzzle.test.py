import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_maps_listing(self):
    puzzle = puz.Puzzle()
    puzzle.process("""$ cd /
$ ls
dir a
123 b.txt
dir c
123 d.txt
""")
    listing = puzzle.root
    files = map(lambda x : x.name, listing.files)
    dirs  = map(lambda x : x.name, listing.dirs)

    self.assertEquals(files, ['b.txt', 'd.txt'])
    self.assertEquals(dirs,  ['a', 'c'])

  def test_puzzle_moves_in_and_out_dirs(self):
    puzzle = puz.Puzzle()
    puzzle.process("""$ cd /
$ ls
dir a
123 b.txt
$ cd a
$ ls
dir c
123 d.txt
$ cd ..
""")
    listing = puzzle.root.dirs[0]
    files = map(lambda x : x.name, listing.files)
    dirs  = map(lambda x : x.name, listing.dirs)

    self.assertEquals(files, ['d.txt'])
    self.assertEquals(dirs,  ['c'])
    self.assertEquals(puzzle.curnode.name, '/')

  def test_puzzle_knows_size_of_files(self):
    puzzle = puz.Puzzle()
    puzzle.process("""$ cd /
$ ls
dir a
123 b.txt
$ cd a
$ ls
dir c
1099 d.txt
$ cd ..
""")
    fileb = puzzle.root.files[0]
    filed = puzzle.root.dirs[0].files[0]

    self.assertEquals(fileb.size, 123)
    self.assertEquals(filed.size, 1099)

if __name__ == '__main__':
    unittest.main()

import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_has_initial_state(self):
    puzzle = puz.Puzzle()
    expected = """.#.
..#
###"""

    self.assertEquals(puzzle.image(), expected)

  def test_puzzle_fragment_initial_to_self(self):
    puzzle = puz.Puzzle()
    expected = """.#.
..#
###"""
    parts = puzzle.fragment()

    self.assertEquals(parts[0][0], expected)

  def test_puzzle_fragment_even_to_2x2(self):
    puzzle = puz.Puzzle()
    initial = """.#..
..#.
.#..
####"""
    puzzle.state = initial
    parts = puzzle.fragment()

    self.assertEquals(parts[0][0], ".#\n..")
    self.assertEquals(parts[0][1], "..\n#.")
    self.assertEquals(parts[1][0], ".#\n##")
    self.assertEquals(parts[1][1], "..\n##")

  def test_puzzle_fragment_mul3_to_3x3(self):
    puzzle = puz.Puzzle()
    initial = """.#.###
..#.##
.#..##
######
..#.##
##.###"""
    puzzle.state = initial
    parts = puzzle.fragment()

    self.assertEquals(parts[0][0], ".#.\n..#\n.#.")
    self.assertEquals(parts[0][1], "###\n.##\n.##")
    self.assertEquals(parts[1][0], "###\n..#\n##.")
    self.assertEquals(parts[1][1], "###\n.##\n###")

  def test_puzzle_loads_patterns(self):
    puzzle = puz.Puzzle()
    puzzle.process("""../.. => ###/###/###
###/###/### => ..../..../..../....
""")

    pattern1 = puzzle.patterns["..\n.."]
    pattern2 = puzzle.patterns["###\n###\n###"]

    self.assertEquals(pattern1, "###\n###\n###")
    self.assertEquals(pattern2, "....\n....\n....\n....")

  def test_puzzle_enhances_chunks(self):
    puzzle = puz.Puzzle()
    puzzle.process("""../.. => ###/###/###
###/###/### => ..../..../..../....
""")

    enhanced = puzzle.enhance("..\n..")

    self.assertEquals(enhanced, "###\n###\n###")

  def test_puzzle_enhances_image(self):
    puzzle = puz.Puzzle()
    puzzle.process("""../.. => ###/###/###
.#./..#/### => ..../..../..../....
""")

    puzzle.enhanceImage()
    expected = """....
....
....
...."""

    self.assertEquals(puzzle.image(), expected)
    puzzle.enhanceImage()
    expected = """######
######
######
######
######
######"""
    self.assertEquals(puzzle.image(), expected)

    

  def test_puzzle_enhances_rotated_2x_matches(self):
    puzzle = puz.Puzzle()
    puzzle.process("""../.# => ###/###/###
###/###/### => ..../..../..../....
""")

    enhanced = puzzle.enhance("#.\n..")

    self.assertEquals(enhanced, "###\n###\n###")

  def test_puzzle_enhances_rotated_3x_matches(self):
    puzzle = puz.Puzzle()
    puzzle.process("""../.# => ###/###/###
#../#../### => ..../..../..../....
""")

    enhanced = puzzle.enhance("###\n..#\n..#")

    self.assertEquals(enhanced, "....\n....\n....\n....")

  def test_puzzle_enhances_hflips(self):
    puzzle = puz.Puzzle()
    puzzle.process("""../.# => ###/###/###
.#./..#/### => ..../..../..../....
""")

    enhanced = puzzle.enhance(".#.\n#..\n###")

    self.assertEquals(enhanced, "....\n....\n....\n....")

  def test_puzzle_enhances_vflips(self):
    puzzle = puz.Puzzle()
    puzzle.process("""../.# => ###/###/###
##./#.#/#.. => ..../..../..../....
""")

    enhanced = puzzle.enhance("""#..
#.#
##.""")

    self.assertEquals(enhanced, "....\n....\n....\n....")
if __name__ == '__main__':
    unittest.main()

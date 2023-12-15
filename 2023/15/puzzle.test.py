import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_char_chunks(self):
    puzzle = puz.Puzzle()
    puzzle.process("""abc,def
""")
    self.assertEqual(puzzle.chunks[0], 'abc')

  def test_puzzle_calculates_hash(self):
    puzzle = puz.Puzzle()
    puzzle.process("""abc,def
""")
    self.assertEqual(puzzle.hash('HASH'), 52)
    self.assertEqual(puzzle.hash('cm-'), 253)
    self.assertEqual(puzzle.hash('ot=9'), 9)

  def test_puzzle_assigns_lense_to_box(self):
    puzzle = puz.Puzzle()
    puzzle.process("""abc,def
""")

    puzzle.execute("ab=2")

    box = puzzle.boxes[puzzle.hash("ab")]

    self.assertEqual(box, [("ab", 2)])
    

  def test_puzzle_updates_lense_in_place(self):
    puzzle = puz.Puzzle()
    puzzle.process("""abc,def
""")

    h = puzzle.hash("ab")
    puzzle.boxes[h].append(("cc", 0))
    puzzle.boxes[h].append(("ab", 100))
    puzzle.boxes[h].append(("dd", 12))

    box = puzzle.boxes[h]
    self.assertEqual(box[1], ("ab", 100))

    puzzle.execute("ab=2")
    self.assertEqual(box[1], ("ab", 2))

  def test_puzzle_minus_removes_a_lens(self):
    puzzle = puz.Puzzle()
    puzzle.process("""abc,def
""")

    h = puzzle.hash("ab")
    puzzle.boxes[h].append(("cc", 0))
    puzzle.boxes[h].append(("ab", 100))
    puzzle.boxes[h].append(("dd", 12))
    puzzle.execute("ab-")
    box = puzzle.boxes[h]

    self.assertEqual(box[1], ("dd", 12))

  def test_puzzle_calcfocus(self):
    puzzle = puz.Puzzle()
    puzzle.process("""abc,def
""")

    h = puzzle.hash("ab")
    puzzle.boxes[h].append(("cc", 0))
    puzzle.boxes[h].append(("ab", 100))
    puzzle.boxes[h].append(("dd", 12))
    box = puzzle.boxes[h]

    self.assertEqual(puzzle.focus(1, box), (1*1*0) + (1*2*100) + (1*3*12))

if __name__ == '__main__':
    unittest.main()

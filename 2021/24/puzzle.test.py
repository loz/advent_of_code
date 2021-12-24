import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_inp(self):
    puzzle = puz.Puzzle()
    puzzle.process("""inp x
inp y
inp z
""")
    puzzle.run("1234567")

    self.assertEqual(puzzle.reg['x'], 1)
    self.assertEqual(puzzle.reg['y'], 2)
    self.assertEqual(puzzle.reg['z'], 3)

  def test_puzzle_add(self):
    puzzle = puz.Puzzle()
    puzzle.process("""add x 1
add y 2
add x y
""")
    puzzle.run("1234567")

    self.assertEqual(puzzle.reg['x'], 3)
    self.assertEqual(puzzle.reg['y'], 2)

  def test_puzzle_mul(self):
    puzzle = puz.Puzzle()
    puzzle.process("""add x 3
add y 2
mul x y
mul x 2
""")
    puzzle.run("1234567")

    self.assertEqual(puzzle.reg['x'], 12)

  def test_puzzle_div(self):
    puzzle = puz.Puzzle()
    puzzle.process("""add x 8
add y 3
div x y
div y y
""")
    puzzle.run("1234567")

    self.assertEqual(puzzle.reg['x'], 2)
    self.assertEqual(puzzle.reg['y'], 1)

  def test_puzzle_mod(self):
    puzzle = puz.Puzzle()
    puzzle.process("""add x 8
add y 3
mod x y
mod y y
""")
    puzzle.run("1234567")

    self.assertEqual(puzzle.reg['x'], 2)
    self.assertEqual(puzzle.reg['y'], 0)

  def test_puzzle_eql(self):
    puzzle = puz.Puzzle()
    puzzle.process("""add x 8
add y 3
eql x y
eql y y
""")
    puzzle.run("1234567")

    self.assertEqual(puzzle.reg['x'], 0)
    self.assertEqual(puzzle.reg['y'], 1)

if __name__ == '__main__':
    unittest.main()

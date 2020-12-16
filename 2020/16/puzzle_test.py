import unittest
import puzzle as puz

EXAMPLE="""class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
"""

class TestPuzzle(unittest.TestCase):

  def test_recognise_valid_number(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)

    self.assertTrue(puzzle.valid(7))
    self.assertTrue(puzzle.valid(3))
    self.assertTrue(puzzle.valid(47))
    self.assertFalse(puzzle.valid(4))
    self.assertFalse(puzzle.valid(55))
    self.assertFalse(puzzle.valid(12))

  def test_recognise_valid_field(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)

    self.assertTrue(puzzle.validField('class', 7))
    self.assertTrue(puzzle.validField('row', 35))
    self.assertFalse(puzzle.validField('seat', 9))

  def test_parse_your_ticket(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)
    
    self.assertEqual(puzzle.yours, [7,1,14])

  def test_parse_other_tickets(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)
    
    self.assertEqual(puzzle.others[0], [7,3,47])
    self.assertEqual(puzzle.others[1], [40,4,50])
    self.assertEqual(puzzle.others[2], [55,2,20])
    self.assertEqual(puzzle.others[3], [38,6,12])

if __name__ == '__main__':
    unittest.main()

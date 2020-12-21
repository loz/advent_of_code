import unittest
import puzzle as puz

EXAMPLE="""mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
"""

class TestPuzzle(unittest.TestCase):

  def test_identifies_ingredients(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)
    
    self.assertIn('dairy', puzzle.ingredients)
    self.assertIn('fish', puzzle.ingredients)
    self.assertIn('soy', puzzle.ingredients)

  def test_identifies_food(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)
    
    self.assertIn('kfcds', puzzle.foods)
    self.assertIn('mxmxvkd', puzzle.foods)
    self.assertIn('trh', puzzle.foods)

  def test_matches_allergen_to_food(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)
    
    self.assertEqual(puzzle.ingredients['dairy'], 'mxmxvkd')
    self.assertEqual(puzzle.ingredients['fish'], 'sqjhc')
    self.assertEqual(puzzle.ingredients['soy'], 'fvjkl')

  def test_count_appearances(self):
    puzzle = puz.Puzzle()
    puzzle.process(EXAMPLE)
    
    self.assertEqual(puzzle.count_appearance(['kfcds', 'nhms', 'sbzzf', 'trh']), 5)

if __name__ == '__main__':
    unittest.main()

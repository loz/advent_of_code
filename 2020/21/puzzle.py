import re

PATTERN=r"^(?P<foods>([a-z]+ )+)\(contains (?P<allergens>([a-z]+, )*([a-z]+))\)$"

class Puzzle:

  def process(self, text):
    ingredients = {}
    items = []
    self.foods = set()
    lines = text.split('\n')
    for line in lines:
      if line.strip() != '':
        food, allergens = self.parse_ingredients(line)
        self.foods |= set(food)
        items += food
        for allergen in allergens:
          if ingredients.has_key(allergen):
            ingredients[allergen] &= set(food)
          else:
            ingredients[allergen] = set(food)
    self.items = items
    #print 'Narrowing'
    narrowing = True
    while narrowing:
      narrowing = False
      singles = filter(lambda a: len(ingredients[a]) == 1, ingredients)
      multies = filter(lambda a: len(ingredients[a]) > 1, ingredients)
      for allergen in multies:
        narrowing = True
        items = ingredients[allergen]
        #print 'Narrow', allergen
        #print allergen, items
        for i in singles:
          items -= ingredients[i]
        ingredients[allergen] = items

    self.ingredients = {}
    for allergen in ingredients:
      self.ingredients[allergen] = list(ingredients[allergen])[0]

  def parse_ingredients(self, line):
    match = re.match(PATTERN, line)
    food = match.group('foods').split(' ')
    food = filter(lambda f: f != '', food)
    allergens = match.group('allergens').split(', ')
    return (food, allergens)

  def count_appearance(self, items):
    total = 0
    for item in items:
      total += self.items.count(item)
    return total

  def result(self):
    foods = map(lambda f: f, self.foods)
    for allergen in self.ingredients:
      item = self.ingredients[allergen]
      print allergen, ' in ', item
      foods.remove(item)
    print 'OK Foods', foods
    print 'Appear', self.count_appearance(foods)
    allergies = self.ingredients.keys()
    allergies.sort()
    danger = map(lambda a: self.ingredients[a], allergies)
    print 'Canonical:', ','.join(danger)


if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

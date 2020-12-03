class Puzzle:

  def process(self, text):
    lines = filter(lambda l : l.strip() != '', text.split())
    self.lines = lines
    self.height = len(lines)
    self.width = len(lines[0])

  def count_trees(self, dx, dy):
    x = 0
    y = 0
    trees = 0
    while y < self.height:
      if self.lines[y][x] == '#':
        trees = trees + 1
      x = (x + dx) % self.width
      y = y + dy
    return trees

  def result(self):
    slopes = [
      (1, 1),
      (3, 1),
      (5, 1),
      (7, 1),
      (1, 2)
    ]
    mul = 1
    for slope in slopes:
      dx, dy = slope
      total = self.count_trees(dx, dy)
      mul = mul * total
      print "Trees Hit: ", slope, total
    print "Multiplied:", mul
if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

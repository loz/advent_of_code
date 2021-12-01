class Puzzle:

  def process(self, text):
    self.increments = 0
    self.last = None
    self.windows = []
    lines = text.split()
    depths = map(lambda l: int(l), lines)
    self.windows = self.sliding_window(depths)
  
  def sliding_window(self, depths):
    rest = depths[0:]
    a = rest[0]
    b = rest[1]
    c = rest[2]
    values = []
    values.append(a + b + c)
    a = b
    b = c
    if rest == []:
      return values
    rest = rest[3:]
    while rest != []:
      c = rest[0]
      rest = rest[1:]
      values.append(a + b + c)
      a = b
      b = c
    return values

  def count_increments(self, depths):
    for depth in depths:
      if self.last != None:
        if depth > self.last:
          self.increments += 1
      self.last = depth


  def result1(self):
    self.count_increments(self.depths)
    print "The total increments =", self.increments

  def result(self):
    self.count_increments(self.windows)
    print "The total increments =", self.increments

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

import sys

class Puzzle:

  def process(self, text):
    self.components = []
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      left, right = line.split('/')
      left = int(left)
      right = int(right)
      self.components.append((left, right))

  def options(self, connection, available=None):
    if available == None:
      available = self.components
    choices = []
    for o in available:
      l, r = o
      if connection == l or connection == r:
        choices.append(o)
    return choices

  def build(self, end, stem, available):
    bridges = []
    options = self.options(end, available)
    for o in options:
      l, r = o
      newstem = stem + [o]
      bridges.append(newstem)
      newavail = [x for x in available if x != o]
      if l == end:
        bridges += self.build(r, newstem, newavail)
      else:
        bridges += self.build(l, newstem, newavail)
    return bridges
    

  def result(self):
    bridges = []
    available = [ch for ch in self.components]
    bridges += self.build(0, [], available)
    longlen = len(max(bridges, key=lambda x: len(x)))
    print 'Longest =', longlen
    strongest = 0
    for bridge in bridges:
      if len(bridge) == longlen:
        strength = 0
        for ch in bridge:
          strength += ch[0] + ch[1]
        print bridge, '=>', strength
        if strength > strongest:
          strongest = strength
    print 'Strongest', strongest


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

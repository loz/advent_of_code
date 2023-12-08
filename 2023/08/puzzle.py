import sys

DIRMAP = {
  'L' : 0,
  'R' : 1
}

class Puzzle:

  def process(self, text):
    self.start = 'AAA'
    directions, *lines = text.split('\n')
    self.directions = [DIRMAP[ch] for ch in directions]
    self.current_dir = 0
    self.nodes = {}
    _, *lines = lines
    for line in lines:
      self.process_line(line)
    self.current = self.start

  def process_line(self, line):
    if line != '':
      node, rest = line.split(' = ')
      rest = rest.replace('(', '')
      rest = rest.replace(')', '')
      lhs, rhs = rest.split(', ')
      self.nodes[node] = (lhs, rhs)

  def walk(self):
    to, nd = self.walk_from(self.current, self.current_dir)
    self.current = to
    self.current_dir = nd
    return to

  def walk_from(self, ff, dd):
    d = self.directions[dd]
    dd = dd + 1
    if dd == len(self.directions):
      dd = 0
    nnext = self.nodes[ff]
    return (nnext[d], dd)


  def result(self):
    self.result2()

  def result2(self):
    starts = []
    for k in self.nodes.keys():
      if k.endswith('A'):
        starts.append(k)
    steps = 0
    ended = False
    current = starts
    direction = 0
    while(not ended):
      ends = list(filter(lambda x: x.endswith('Z'), current))
      print(current, ends, len(current), len(ends))
      if len(ends) == len(current):
        ended = True
        break
      nexts = []
      for loc in current:
        nnn, nd = self.walk_from(loc, direction)
        nexts.append(nnn)
      steps = steps + 1
      current = nexts
      direction = nd

    print('Steps', steps)

  def result1(self):
    print(self.start)
    current = self.start
    steps = 0
    while(current != 'ZZZ'):
      current = self.walk()
      print('->', current)
      steps = steps + 1
    print('Total', steps)



if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

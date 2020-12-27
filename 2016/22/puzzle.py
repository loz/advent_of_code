import re
import itertools

NODE = r".*node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T.*"
#NODE = r".*node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+).*"

class Puzzle:

  def process(self, text):
    lines = text.split('\n')
    self._grid = {}
    for line in lines:
      if line.startswith('/dev/grid/'):
        self.parse_node(line)
  
  def parse_node(self, line):
    matches = re.match(NODE, line)
    x, y, size, used, avail = matches.groups()
    self.set_grid(int(x),int(y), {'size':int(size), 'used':int(used), 'avail':int(avail)})

  def set_grid(self, x, y, values):
    if self._grid.has_key(y):
      self._grid[y][x] = values
    else:
      self._grid[y] = {x:values}

  def grid(self, x, y):
    if self._grid.has_key(y):
      return self._grid[y][x]
    else:
      return None

  def _viable(self, pair):
    a, b = pair
    a = a[1]
    b = b[1]
    if a['used'] < b['avail'] and a['used'] != 0:
      return True
    if b['used'] < a['avail'] and b['used'] != 0:
      return True
    return False

  def result(self):
    nodes = []
    for y in self._grid:
      for x in self._grid[y]:
        nodes.append(((x, y), self._grid[y][x]))
    pairs = itertools.combinations(nodes, 2)
    viable = filter(lambda x: self._viable(x), pairs)
    print 'Viable', len(viable)

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

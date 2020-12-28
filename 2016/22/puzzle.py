import re
import itertools
import copy

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
    self.set_grid(int(x),int(y), {'size':int(size), 'used':int(used), 'avail':int(avail), 'goal':False})

  def set_grid(self, x, y, values):
    self._grid[(x,y)] = values

  def grid(self, x, y):
    return self._grid[(x,y)]

  def _viable(self, pair):
    a, b = pair
    a = a[1]
    b = b[1]
    if a['used'] < b['avail'] and a['used'] != 0:
      return True
    if b['used'] < a['avail'] and b['used'] != 0:
      return True
    return False

  #def result1(self):
  #  nodes = []
  #  for y in self._grid:
  #    for x in self._grid[y]:
  #      nodes.append(((x, y), self._grid[y][x]))
  #  pairs = itertools.combinations(nodes, 2)
  #  viable = filter(lambda x: self._viable(x), pairs)
  #  print 'Viable', len(viable)

  def get_size(self):
    keys = self._grid.keys()
    height = max(keys, key=lambda x: x[1])[1]
    width = max(keys, key=lambda x: x[0])[0]
    self.height = height
    self.width = width
    return (width, height)

  def empty_nodes(self, grid):
    empty = []
    for loc in grid:
      if grid[loc]['used'] == 0:
        empty.append(loc)
    return empty

  def neighbours(self, loc):
    x, y = loc
    deltas = [(-1, 0), (1,0), (0,-1), (0,1)]
    neighbours = []
    for dxdy in deltas:
      dx, dy = dxdy
      xdx = x + dx
      ydy = y + dy
      if xdx >= 0 and xdx <= self.width and ydy >=0 and ydy <= self.height:
        neighbours.append((xdx,ydy))
    return neighbours

  def can_move(self, src, dst, grid):
    srcnode = grid[src]
    dstnode = grid[dst]
    return dstnode['avail'] >= srcnode['used']

  def gen_moves(self, empty, neighbours, grid):
    moves = []
    for node in neighbours:
      ngrid = copy.deepcopy(grid)
      srcnode = ngrid[node]
      dstnode = ngrid[empty]
      data = srcnode['used']
      goal = srcnode['goal']
      srcnode['used'] = 0
      srcnode['avail'] += data
      dstnode['used'] = data
      dstnode['avail'] += data
      srcnode['goal'] = dstnode['goal']
      dstnode['goal'] = goal
      moves.append((node, ngrid))
    return moves

  def hash(self, option):
    return str(option)

  def goal_hit(self, grid):
    node = grid[(0,0)]
    return node['goal']

  def dump(self, grid):
    for y in grid:
      for x in grid[y]:
        n = grid[y][x]
        g = ''
        if n['goal'] :
          g = 'G'
        print n['used'], '/', n['size'], g,  '--',
      print ''

  def result(self):
    grid = self._grid
    modified = []
    width, height = self.get_size()
    print width, height
    grid[(width,0)]['goal'] = True
    print grid[(width, 0)]
    empty = self.empty_nodes(grid)[0]
    start = (empty, grid)
    head = [start]
    discovered = {self.hash(start): True}
    tail = []
    depth = 0
    while len(head) > 0:
      empty, grid  = head.pop(0)
      #print empty
      #self.dump(grid)
      if self.goal_hit(grid):
        print 'Goal Reached', depth
        return
      neighbours = self.neighbours(empty)
      neighbours = filter(lambda x: self.can_move(x,empty,grid), neighbours)
      moves = self.gen_moves(empty, neighbours, grid)
      for move in moves:
        h = self.hash(move)
        if not discovered.has_key(h):
          tail.append(move)
          discovered[h] = True
      if len(head) == 0:
        depth += 1
        print 'Depth', depth, len(tail)
        head = tail
        tail = []

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

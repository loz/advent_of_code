import sys
import heapq
from collections import defaultdict

DELTAS = [
  #top->bottom
  (-1,0), (1,0), 
  #left->right
  (0, -1), (0, 1)
]

class Creature:
  def __init__(self, puzzle, x, y):
    self.puzzle = puzzle
    self.x = x
    self.y = y

  def open_squares(self):
    squares = []
    for d in DELTAS:
      dx, dy = d
      nx = self.x+dx
      ny = self.y+dy
      if self.puzzle.item_at(nx, ny) == '.':
        squares.append((nx, ny))
    return squares

  def gen_move(self):
    targets = set()
    for e in self.enemies():
      for t in e.open_squares():
        targets.add(t)
    best = sys.maxsize
    best_paths = []
    for t in targets:
      path = self.puzzle.shortest_path((self.x,self.y), t)
      if not self.puzzle.path_clear(path):
        path = None
        #print 'TODO: find alternate path'
      if path:
        if len(path) < best:
          best = len(path)
          best_paths = [path]
        elif len(path) == best:
          best_paths.append(path)
        #print (self.x, self.y), '->', t, 'shortest path', path
    #print 'Best', best, best_paths
    if len(best_paths) == 1:
      return best_paths[0][0]
    elif len(best_paths) == 0:
      return None
    else:
      #print best_paths
      raise 'Unimplemented multi option'

class Goblin(Creature):
  def enemies(self):
    return [self.puzzle.elves[e] for e in self.puzzle.elves]

class Elf(Creature):
  def enemies(self):
    return [self.puzzle.goblins[e] for e in self.puzzle.goblins]

class Puzzle:

  def process(self, text):
    self.map = []
    self.elves = {}
    self.goblins = {}
    self.op_cache = {}
    y = 0
    for line in text.split('\n'):
      self.process_line(line, y)
      y+=1
    self.width = len(self.map[0])
    self.height = y

  def process_line(self, line, y):
    if line != '':
      row = ''
      for x in range(len(line)):
        ch = line[x]
        if ch == '#' or ch == '.':
          row += ch
        elif ch == 'G':
          row += '.'
          self.goblins[(x,y)] = Goblin(self, x, y)
        elif ch == 'E':
          row += '.'
          self.elves[(x,y)] = Elf(self, x, y)
      self.map.append(row)
  
  def shortest_path(self, start, end):
    #print 'SP', start, end
    #Optimistic paths cache
    op = self.empty_astar(start, end)
    return op

  def path_clear(self, path):
    for node in path:
      if self.item_at(node[0], node[1]) != '.':
        return False
    return True

  def e_ah(self, start, end):
    ax, ay = start
    bx, by = end
    return abs(bx-ax) + abs(by-ay)

  def op_options(self, loc):
    squares = []
    for d in DELTAS:
      dx, dy = d
      nx = loc[0]+dx
      ny = loc[1]+dy
      if self.item_at(nx, ny) != '#':
        squares.append((nx, ny))
    return squares

  def empty_astar(self, start, end):
    if self.op_cache.get((start, end), False):
      return self.op_cache[(start, end)]
    #print 'Gen astar cache'
    g_score = defaultdict(lambda: sys.maxsize)
    f_score = defaultdict(lambda: sys.maxsize)
    g_score[start] = 0
    start_h = self.e_ah(start, end)
    f_score[start] = start_h
    pq = []
    heapq.heapify(pq)
    heapq.heappush(pq, [(start_h, start_h), start])
    paths = {}
    while pq:
      score, loc = heapq.heappop(pq)
      if loc == end:
        #print 'Reached End'
        break
      options = self.op_options(loc)
      for option in options:
        g_s = g_score[loc]+1
        a_h = self.e_ah(option, end)
        f_s = g_s + a_h

        if f_s < f_score[option]:
          g_score[option] = g_s
          f_score[option] = f_s
          heapq.heappush(pq, [(f_s, a_h), option])
          paths[option] = loc

    fwdpath = {}
    node = end
    path = []
    while node != start:
      fwdpath[paths[node]] = node
      #print [node, end], path
      self.op_cache[(node, end)] = path + []
      path = [node] + path
      node = paths[node]
    return path

  def item_at(self, x, y):
    if self.elves.get((x,y), False):
      return self.elves[(x,y)]
    elif self.goblins.get((x,y), False):
      return self.goblins[(x,y)]
    return self.map[y][x]

  def result(self):
    pass



if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

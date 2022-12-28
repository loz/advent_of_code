import sys
import heapq
from collections import defaultdict

DELTAS = [
  #top
  (0, -1), 
  #left->right
  (-1,0), (1,0), 
  #->bottom
  (0, 1),
]

def cmp_scan(a, b):
  if a[1] < b[1]:
    return -1
  elif a[1] == b[1]:
    return -1 if a[0] < b[0] else 1
  else:
    return 1

def cmp_targets(a, b):
  if a.hitpoints < b.hitpoints:
    return -1
  elif a.hitpoints == b.hitpoints:
    al = (a.x, a.y)
    bl = (b.x, b.y)
    return cmp_scan(al, bl)
  else:
    return 1
 
class Creature:
  def __init__(self, puzzle, x, y):
    self.puzzle = puzzle
    self.x = x
    self.y = y
    self.hitpoints = 200
    self.attack = 3

  def health(self):
    return self.ch() + '(' + str(self.hitpoints) + ')'

  def isdead(self):
    return self.hitpoints <= 0

  def strike(self):
    targets = []
    for d in DELTAS:
      dx, dy = d
      nx = self.x+dx
      ny = self.y+dy
      item = self.puzzle.item_at(nx, ny)
      if isinstance(item, Creature):
        if self.is_elf() and not item.is_elf():
          targets.append(item)
        elif not self.is_elf() and item.is_elf():
          targets.append(item)
    targets = sorted(targets, cmp_targets)
    if len(targets) > 0:
      enemy = targets[0]
      enemy.hitpoints -= self.attack
      if enemy.hitpoints <= 0:
        enemy.remove()

  def set_loc(self, loc):
    self.x = loc[0]
    self.y = loc[1]

  def open_squares(self):
    squares = []
    for d in DELTAS:
      dx, dy = d
      nx = self.x+dx
      ny = self.y+dy
      if self.puzzle.item_at(nx, ny) == '.':
        squares.append((nx, ny))
    return squares

  def next_to_enemy(self):
    enem = self.enemy_locations()
    squares = []
    for d in DELTAS:
      dx, dy = d
      nx = self.x+dx
      ny = self.y+dy
      if (nx, ny) in enem:
        return True
    return False

  def gen_move(self):
    if self.next_to_enemy():
      return None
    targets = set()
    enemies = self.enemies()
    if len(enemies) == 0:
      return 'NoTargets'

    for e in enemies:
      for t in e.open_squares():
        targets.add(t)
    best = sys.maxsize
    best_paths = []
    starts = self.open_squares()
    for t in targets:
      for s in starts:
        path = self.puzzle.shortest_path(s, t)
        if not self.puzzle.path_clear(path):
          path = self.puzzle.alternate_path(s,t)
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
      for s in starts:
        for path in best_paths:
          if s == path[0]:
            return s

class Goblin(Creature):
  def enemies(self):
    return [self.puzzle.elves[e] for e in self.puzzle.elves]

  def enemy_hash(self):
    return self.puzzle.elves

  def enemy_locations(self):
    return self.puzzle.elves.keys()

  def is_elf(self):
    return False

  def ch(self):
    return u"\u001b[31mG"

  def remove(self):
    del self.puzzle.goblins[(self.x, self.y)]

class Elf(Creature):
  def enemies(self):
    return [self.puzzle.goblins[e] for e in self.puzzle.goblins]

  def enemy_hash(self):
    return self.puzzle.goblins

  def enemy_locations(self):
    return self.puzzle.goblins.keys()

  def is_elf(self):
    return True

  def ch(self):
    return u"\u001b[32mE"

  def remove(self):
    del self.puzzle.elves[(self.x, self.y)]

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
    self.height = y-1

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
    if op == None:
      return None
    return [start] + op

  def alternate_path(self, start, end):
    op = self.full_astar(start, end)
    if op == None:
      return None
    return [start] + op

  def path_clear(self, path):
    for node in path:
      if self.item_at(node[0], node[1]) != '.':
        return False
    return True

  def a_h(self, start, end):
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

  def options(self, loc):
    squares = []
    for d in DELTAS:
      dx, dy = d
      nx = loc[0]+dx
      ny = loc[1]+dy
      if self.item_at(nx, ny) == '.':
        squares.append((nx, ny))
    return squares

  def empty_astar(self, start, end):
    return self.gen_astar(start, end, self.op_cache, self.op_options)

  def full_astar(self, start, end):
    return self.gen_astar(start, end, {}, self.options)

  def gen_astar(self, start, end, cache, op_fn):
    if cache.get((start, end), False):
      return cache[(start, end)]
    #print 'Gen astar cache', (start, end)
    g_score = defaultdict(lambda: sys.maxsize)
    f_score = defaultdict(lambda: sys.maxsize)
    g_score[start] = 0
    start_h = self.a_h(start, end)
    f_score[start] = start_h
    pq = []
    heapq.heapify(pq)
    heapq.heappush(pq, [(start_h, start_h), start])
    paths = {}
    found = False
    while pq:
      score, loc = heapq.heappop(pq)
      if loc == end:
        found = True
        break
      options = op_fn(loc)
      for option in options:
        g_s = g_score[loc]+1
        a_h = self.a_h(option, end)
        f_s = g_s + a_h
        
        if f_s < f_score[option]:
          g_score[option] = g_s
          f_score[option] = f_s
          heapq.heappush(pq, [(f_s, a_h), option])
          paths[option] = loc

    if not found:
      return None

    fwdpath = {}
    node = end
    path = []
    while node != start:
      fwdpath[paths[node]] = node
      #print [node, end], path
      cache[(node, end)] = path + []
      path = [node] + path
      node = paths[node]
    return path

  def item_at(self, x, y):
    if self.elves.get((x,y), False):
      return self.elves[(x,y)]
    elif self.goblins.get((x,y), False):
      return self.goblins[(x,y)]
    return self.map[y][x]
  

  def tick(self):
    locs = self.elves.keys() + self.goblins.keys()
    locs = sorted(locs, cmp=cmp_scan)
    bots = [self.item_at(loc[0], loc[1]) for loc in locs]
    for bot in bots:
      loc = (bot.x, bot.y)
      if bot.isdead():
        continue
      mv = bot.gen_move()
      if mv == 'NoTargets':
        return False
      if mv == None:
        mv = loc
      bot.set_loc(mv)
      if bot.is_elf():
        del self.elves[loc]
        self.elves[mv] = bot
      else:
        del self.goblins[loc]
        self.goblins[mv] = bot
      bot.strike()
      #self.dump()
    return True

  def dump(self):
    print u"\u001b[0;0H"
    print 
    for y in range(self.height):
      bots = []
      for x in range(self.width):
        item = self.item_at(x,y)
        if isinstance(item, Creature):
          bots.append(item)
          sys.stdout.write(item.ch())
        elif item == '#':
          sys.stdout.write(u"\u001b[33m#")
        else:
          sys.stdout.write(u"\u001b[0m.")
      print u"\u001b[K",
      for bot in bots:
        print u"\u001b[0m", bot.health(),
      print u"\u001b[0m"

  def victory(self):
    return len(self.elves.keys()) == 0 or len(self.goblins.keys()) == 0

  def combat(self):
    rnd = 0
    self.dump()
    while not self.victory():
      if self.tick():
        rnd += 1
      self.dump()
      print 'After', rnd, 'FULL rounds:'
    outcome = 0
    for e in self.elves:
      outcome += self.elves[e].hitpoints
    for g in self.goblins:
      outcome += self.goblins[g].hitpoints
    print 'Outcome', outcome, '*', rnd, '=', outcome * rnd

  def result(self):
    self.combat()



if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

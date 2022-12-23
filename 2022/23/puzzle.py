import sys
from collections import defaultdict

DELTAS = {
  'n': [(-1,-1), (0, -1), (1, -1)],
  's': [(-1, 1), (0,  1), (1,  1)],
  'w': [(-1,-1), (-1, 0), (-1, 1)],
  'e': [( 1,-1), ( 1, 0), ( 1, 1)]
}

class Puzzle:

  def process(self, text):
    self.locations = {}
    self.priority = ['n', 's', 'w', 'e']
    curline = 0
    for line in text.split('\n'):
      self.process_line(line, curline)
      curline += 1

  def process_line(self, line, y):
    if line != '':
      for x in range(len(line)):
        if line[x] == '#':
          self.locations[(x,y)] = True

  def neighbours(self, direction, loc):
    x, y = loc
    d = DELTAS[direction]
    found = []
    for dd in d:
      dx, dy = dd
      if self.elf_at(x+dx, y+dy):
        found.append((x+dx, y+dy))
    return found

  def tick(self):
    new_locations = defaultdict(list)
    for elf in self.locations:
      n = self.neighbours('n', elf)
      s = self.neighbours('s', elf)
      w = self.neighbours('w', elf)
      e = self.neighbours('e', elf)
      #print '?', elf, n, s, w, e
      if n + s + w + e == []:
        new_locations[elf].append(elf)
      else:
        nbrs = {'n':n, 's':s, 'e':e, 'w':w}
        movs = {'n': (0,-1), 's':(0,1), 'e':(1,0), 'w':(-1,0)}
        for d in self.priority:
          if not nbrs[d]:
            x,y = elf
            dx, dy = movs[d]
            new_locations[(x+dx, y+dy)].append(elf)
            break
        else:
          new_locations[elf].append(elf)
    self.locations = {}
    #print new_locations
    moved = 0
    for loc in new_locations:
      if len(new_locations[loc]) == 1:
        #will_move
        self.locations[loc] = True
        if loc != new_locations[loc][0]:
          moved += 1
      else:
        #stay in source
        for oloc in new_locations[loc]:
          self.locations[oloc] = True
    #rotate priority
    p = self.priority.pop(0)
    self.priority.append(p)
    return moved

  def elf_at(self, x, y):
    return self.locations.get((x,y), False)

  def dump(self):
    minx = 0
    maxx = 0
    miny = 0
    maxy = 0
    for loc in self.locations:
      x, y = loc
      minx = min(x, minx)
      miny = min(y, miny)
      maxx = max(x, maxx)
      maxy = max(y, maxy)
    print (minx, miny), (maxx, maxy)
    elfcount = 0
    spacecount = 0
    for y in range(miny, maxy+1):
      for x in range(minx, maxx+1):
        if self.elf_at(x,y):
          sys.stdout.write('#')
          elfcount +=1
        else:
          sys.stdout.write('.')
          spacecount += 1
      print
    print elfcount, 'elfs'
    print spacecount, 'spaces'

  def result(self):
    print '='*10
    #self.dump()
    movecount = 99
    rnd=0
    while movecount != 0:
      movecount = self.tick()
      print 'Round', rnd+1, 'moved', movecount
      rnd += 1
    #for rnd in range(21):
    #  print '=== Round', rnd+1, ' ==='
    #  movecount = self.tick()
    #  #self.dump()
    #  print '===', movecount, 'moved ==='



if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

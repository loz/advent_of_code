import sys

DELTA = [
  (-1, 0), (1, 0),
  (0,-1), (0,1)
]

class Puzzle:

  def process(self, text):
    self.map = {}
    for y, line in enumerate(text.split('\n')):
      self.process_line(y, line)
    self.height = y-1

  def process_line(self, y, line):
    if line != '':
      for x, ch in enumerate(line):
        if ch == 'S':
          self.start = (x, y)
          ch = '.'
        self.map[(x,y)] = ch
      self.width = x

  def at(self, x, y):
    x = x % (self.width+1)
    y = y % (self.height+1)
    return self.map[(x,y)]

  def r_walk(self, loc, steps, seen, visited):
    if steps == 0:
      visited[loc] = True
    else:
      x, y = loc
      for dx, dy in DELTA:
        nx, ny = x+dx, y+dy
        #print((nx,ny), self.at(nx,ny), steps)
        if self.at(nx,ny) == '.':
          if (nx,ny, steps-1) not in seen:
            seen[(nx,ny,steps-1)] = True
            self.o_walk((nx,ny), steps-1, seen, visited)

  def rr_walk(self, loc, steps):
    if steps == 0:
      return {(0,0):True}

    x, y = loc
    mx = x % (self.width+1)
    my = y % (self.height+1)

    if ((mx,my), steps) in self.cache:
      vset = self.cache[((mx, my), steps)]
      return vset

    udeltas = {}
    for dx, dy in DELTA:
      nx, ny = x+dx, y+dy
      nloc = (nx, ny)
      if self.at(nx,ny) == '.':
        #if (nx,ny, steps-1) not in seen:
        #  seen[(nx,ny,steps-1)] = True
        #  total = total.union(self.rr_walk(nloc, steps-1, seen, visited))
        deltas = self.rr_walk(nloc, steps-1)
        #offset these with the delta we are at
        for ddy, ddx in deltas:
          udeltas[(ddy+dx, ddx+dy)] = True

    
    #print('Caching', (mx,my), '@', steps, udeltas)
    self.cache[((mx,my), steps)] = udeltas
    return udeltas

  def o_walk(self, start, steps, seen, visited):
    current = steps
    tovisit = [(start, steps, [])]
    while tovisit:
      loc, step, path = tovisit.pop(0)
      if step == 0:
        for o, l in enumerate(path):
          k = (l, o+1)
          c = visited.get(k, 0)
          c += 1
          visited[k] = c
      else:
        x, y = loc
        for dx, dy in DELTA:
          nx, ny = x+dx, y+dy
          #print((nx,ny), self.at(nx,ny), steps)
          #nx = nx % (self.width+1)
          #ny = ny % (self.height+1)
          #print(x, y, mx, my)
          if self.at(nx,ny) == '.':
            if (nx,ny, step-1) not in seen:
              seen[(nx,ny,step-1)] = True
              tovisit.append(((nx,ny), step-1, [loc] + path))
             #tovisit.append(((nx,ny), step-1))
    return visited[(start, steps)]

  def infinite_walk(self, loc, steps):
    #print('Start', loc, steps)
    self.cache = {}
    locs = self.rr_walk(loc, steps)
    #print(locs)
    return len(locs)

  def walk(self, loc, steps):
    visited = {}
    seen = {}
    self.r_walk(loc, steps, seen, visited)
    return visited.keys()

  def result(self):
    self.result2()

  def result1(self):  
    steps = [6, 64]
    for s in steps:
      places = self.walk(self.start, s)
      print(s, len(places))

  def result2(self):  
    steps = [6,10, 50, 100, 500, 1000, 5000]
    for s in steps:
      count = self.infinite_walk(self.start, s)
      print(s, count)



if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

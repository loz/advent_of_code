import sys
import heapq

DELTA = [
  (-1, 0), (1, 0),
  (0,-1), (0,1)
]

class Puzzle:

  def process(self, text):
    self.map = {}
    for y, line in enumerate(text.split('\n')):
      self.process_line(y, line)
    self.height = y
    print('W:', self.width, 'H:', self.height)

  def process_line(self, y, line):
    if line != '':
      for x, ch in enumerate(line):
        if ch == 'S':
          self.start = (x, y)
          ch = '.'
        self.map[(x,y)] = ch
      self.width = x+1

  def at(self, x, y):
    x = x % (self.width)
    y = y % (self.height)
    return self.map[(x,y)]

  def dumpgrid(self, gridid, visited, steps, start):
    print('==== GRID', gridid, '=======')
    #oddeven = gridid[2]
    if steps % 2 == 0:
      oddeven = 0
    else:
      oddeven = 1
    total = 0
    for y in range(self.height):
      for x in range(self.width):
        if (x,y) in visited:
          d = visited[(x,y)]
          if d == steps:
            total += 1
            if (x,y) == start:
              sys.stdout.write('S')
            else:
              sys.stdout.write('O')
          elif d < steps and (d % 2 == oddeven):
          #elif d < steps and (d % 2 == 0):
            total += 1
            if (x,y) == start:
              sys.stdout.write('S')
            else:
              sys.stdout.write('O')
          elif (x,y) == start:
            sys.stdout.write('s')
          else:
            #sys.stdout.write(str(d))
            sys.stdout.write('_')
        elif (x,y) == start:
          sys.stdout.write('s')
        else:
          sys.stdout.write(self.at(x, y))
      sys.stdout.write('\n')
    print('Total:', total)

  def countplots(self, gridid, visited, steps):
    if steps % 2 == 0:
      oddeven = 0
    else:
      oddeven = 1
    total = 0
    for d in visited:
      dd = visited[d]
      if dd == steps or (dd < steps and (dd % 2 == oddeven)):
        total +=1
    return total
    

  def flood(self, loc, steps):
    grids = [(loc, steps, (0, 0, 0))]
    seen = [(0,0)]
    visited = 0
    while grids:
      loc, stepsleft, gridid = grids.pop(0)
      print('Flooding', gridid, 'with', stepsleft, 'steps, from', loc)
      exits, distances = self.grid_flood(loc, stepsleft)
      #print(distances)
      visited += self.countplots(gridid, distances, stepsleft)
      self.dumpgrid(gridid, distances, stepsleft, loc)

      for direction in exits:
        print(direction, len(exits[direction]))
        mindistance = steps*10
        bestloc = None
        for option in exits[direction]:
          eloc, distance = option
          if mindistance > distance:
            mindistance = distance
            bestloc = eloc
        if bestloc != None:
          #print(direction, 'Best Exit ->', bestloc, mindistance)
          gx, gy, oddeven = gridid
          dx, dy = direction
          ngx, ngy = gx+dx, gy+dy
          remaining = stepsleft-mindistance
          if (ngx, ngy) not in seen:
            seen.append((ngx, ngy))
            grids.append( (bestloc, remaining, (ngx, ngy, 1-oddeven))   )
        else:
          #print(direction, 'No Exit')
          pass
    return visited

  def grid_flood(self, loc, steps):
    exits = {}
    for d in DELTA:
      exits[d] = []

    tovisit = []
    heapq.heapify(tovisit)
    heapq.heappush(tovisit, [0, loc, steps])

    visited = {}
    while tovisit:
      distance, loc, remaining = heapq.heappop(tovisit)
      x, y = loc

      if remaining == 0:
        pass
        #visited[(x, y)] = distance
      else:
        #print('V', (x, y), steps, distance)
        for dx, dy in DELTA:
          nx, ny = x+dx, y+dy
          if self.at(nx, ny) == '.':
            if nx < 0 or ny < 0 or nx >= self.width or ny >= self.height:
              #An exit hit
              nx = nx % (self.width)
              ny = ny % (self.height)
              #print('Exit', (nx, ny), distance+1, '->', (dx, dy))
              exits[(dx, dy)].append( ((nx,ny), distance+1) )
            else:
              if (nx, ny) not in visited and remaining > 0:
                visited[(nx, ny)] = distance + 1
                heapq.heappush(tovisit, [distance+1, (nx, ny), remaining-1 ] )

    return exits, visited

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
    mx = x % (self.width)
    my = y % (self.height)

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
          #nx = nx % (self.width)
          #ny = ny % (self.height)
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
    #steps = [6,10, 50, 100, 500, 1000, 5000]
    steps = [6,10]
    for s in steps:
      count = self.flood(self.start, s)
      print(s, count)
    

  def result2_brute(self):  
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

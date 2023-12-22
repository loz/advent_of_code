import sys
import heapq
import math
from numpy import polyfit

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
          total += 1
          if (x,y) == start:
            sys.stdout.write('S')
          else:
            sys.stdout.write('O')
        elif (x,y) == start:
          sys.stdout.write('s')
        else:
          sys.stdout.write(self.at(x, y))
      sys.stdout.write('\n')
    print('Total:', total)

  def countplots(self, gridid, visited, steps):
    return len(visited.keys())
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
    grids = [(loc, steps, (0, 0))]
    seen = {((0,0), steps, loc):True}
    known = {}
    while grids:
      loc, stepsleft, gridid = grids.pop(0)
      if gridid not in known:
        known[gridid] = {}
      current = known[gridid]

      #print('Flooding', gridid, 'with', stepsleft, 'steps, from', loc)
      exits, distances = self.grid_flood(loc, stepsleft, current)
      #print(distances)
      #self.countplots(gridid, distances, stepsleft)
      #self.dumpgrid(gridid, distances, stepsleft, loc)

      for direction in exits:
        for option in exits[direction]:
          eloc, distance = option
          gx, gy = gridid
          dx, dy = direction
          ngx, ngy = gx+dx, gy+dy
          ngid = (ngx, ngy)
          remaining = stepsleft-distance
          k = (ngid, remaining, eloc)
          if k not in seen:
            seen[k] = True
            grids.append( (eloc, remaining, ngid) )
          #grids.append( (eloc, remaining, ngid) )
        #print(direction, len(exits[direction]))
        #mindistance = steps*10
        #bestloc = None
        #for option in exits[direction]:
        #  eloc, distance = option
        #  if mindistance > distance:
        #    mindistance = distance
        #    bestloc = eloc
        #if bestloc != None:
        #  #print(direction, 'Best Exit ->', bestloc, mindistance)
        #  gx, gy = gridid
        #  dx, dy = direction
        #  ngx, ngy = gx+dx, gy+dy
        #  remaining = stepsleft-mindistance
        #  if (ngx, ngy) not in seen:
        #    seen.append((ngx, ngy))
        #    grids.append( (bestloc, remaining, (ngx, ngy))   )
        #else:
        #  #print(direction, 'No Exit')
        #  pass
    visited = 0
    print('Virtual Grids', len(known.keys()))
    for grid in known.keys():
      visited += len(known[grid])
    return visited

  def calculate_distances(self):
    tovisit = []
    heapq.heapify(tovisit)
    heapq.heappush(tovisit, [0, self.start])
    distances = {}
    while tovisit:
      distance, loc = heapq.heappop(tovisit)
      x, y = loc
      for dx, dy in DELTA:
        nx, ny = x+dx, y+dy
        if self.at(nx, ny) == '.':
          if nx < 0 or ny < 0 or nx >= self.width or ny >= self.height:
            pass
          else:
            if (nx, ny) not in distances:
              distances[(nx, ny)] = distance + 1
              heapq.heappush(tovisit, [distance+1, (nx, ny) ] )
    return distances
    
    
  def grid_flood(self, loc, steps, visited):
    exits = {}
    for d in DELTA:
      exits[d] = []

    tovisit = []
    heapq.heapify(tovisit)
    heapq.heappush(tovisit, [0, loc, steps])
    seen = {}

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
              #print('Exit', (nx, ny), distance+1, '->', (dx, dy), remaining-distance)
              exits[(dx, dy)].append( ((nx,ny), distance+1) )
            else:
              if (nx, ny) not in seen: #and remaining > 0:
                seen[(nx, ny)] = True
                if remaining % 2 == 1:
                  visited[(nx, ny)] = True
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

  def bf_walk(self, loc, steps):
    if steps % 2 == 0:
      oddeven = 1
    else:
      oddeven = 0
    #breadth first walk of map
    reached = {}
    stopable = {}
    tovisit = [(loc, steps, 0)]
    while tovisit:
      loc, remaining, distance = tovisit.pop(0)
      if remaining == 0:
        reached[loc] = distance
        stopable[loc] = True
      else:
        x, y = loc
        for dx, dy in DELTA:
          nx, ny = x+dx, y+dy
          if self.at(nx,ny) == '.':
            if (nx,ny) not in reached:
              reached[(nx,ny)] = distance
              if (distance) % 2 == oddeven:
                stopable[(nx, ny)] = True
              tovisit.append(((nx,ny), remaining-1, distance+1))
    return stopable
    return reached


  def infinite_walk_o(self, loc, steps):
    #print('Start', loc, steps)
    seen = {}
    visited = {}
    self.cache = {}
    reachable = self.bf_walk(loc, steps)
    return len(reachable)

  def walk(self, loc, steps):
    visited = {}
    seen = {}
    self.r_walk(loc, steps, seen, visited)
    return visited.keys()

  def result(self):
    self.result2()

  def result2_pfit(self, steps):
    w = self.width
    if steps < 2*w:
      return self.infinite_walk_o(self.start, steps)
    else:
      #print('Large!')
      rem = steps % w
      if rem == 0:
        rem = w
      #print('Simulating..')
      data = []
      for n in range(3):
        x = (w *n) + rem
        y = self.infinite_walk_o(self.start, x)
        #print((x, y))
        data.append([x,y])
      print('Approximating:', data)
      a, b, c = self.fit_quadratic(data)
      #print('C:', (a, b, c))
      n = steps
      #print('N:', n)
      val = a * n **2 +  b * n + c
      ival = int(val)
      #print('Steps:', n, '->', ival)
      return ival

  def result2(self):
    steps = [6,10, 50, 100, 500, 1000, 5000, 26501365]
    #steps = [26501365]
    for step in steps:
      v = self.result2_pfit(step)
      print(step, '=>', v)
    return

    target = 26501365
    #Work out 3 solutions by brute
    steps = []
    w = self.width
    rem = target % w
    print('Remainder', rem)
    for n in range(3):
      steps.append( (((n+1)*w)+rem) )
    print('Simulating..')
    known = []
    #steps = [6,10, 50, 100, 500, 1000, 5000]
    for s in steps:
      count = self.infinite_walk_o(self.start, s)
      #print(s, count)
      known.append((s, count))

    print('Fitting Quadratic')
    a, b, c = self.fit_quadratic(known)
    steps = [6,10, 50, 100, 500, 1000, 5000, 26501365]
    for step in steps:
      # ax^2 + bx + c
      val = ((a*step)*(a*step)) + (b*step) + c
      ival = int(val)
      print('Steps:', step, '->', ival)

  def fit_quadratic(self, pairs):
    xs, ys = zip(*pairs)
    coefficients = polyfit(xs, ys, 2)
    #print('Coefficients', coefficients)
    return coefficients
    a = (ys[-1] - 2*ys[-2] + ys[-3]) / (xs[-1]**2 - 2*xs[-2]**2 + xs[-3]**2)
    b = (ys[-1] - ys[-2] - a * xs[-1] ** 2 + a * xs[-2]**2) / (xs[-1] - xs[-2])
    c = ys[-1] - a * xs[-1] ** 2 - b * xs[-1]
    #print('a, b, c', (a, b, c))
    return a, b, c

  def result2_old(self):
    steps = [6,10, 50, 100, 500, 1000, 5000, 26501365]
    for step in steps:
      self.result2_manhattan(step)

  def result1(self):  
    steps = [6, 64]
    for s in steps:
      places = self.walk(self.start, s)
      print(s, len(places))

  def result2_manhattan(self, steps):
    print('Calculate for', steps)
    #Each step folows manhattan distance (effectively)
    #            O                      O
    #      O    OOO              O     O O
    # O   OOO  OOOOO  ->   O    O O   O O O   
    #      O    OOO              O     O O
    #            O                      O
    #Except you can only stop on alternate steps
    #Each REPLICA of the grid also manhatten
    # -> Alternating Odd Even or Even/Odd based on step count
    #            #                      E
    #      #    ###              E     EOE
    # #   ###  #####  ->   #    EOE   EOEOE   
    #      #    ###              E     EOE
    #            #                      E
    # On the INSIDE all possible squares are visited
    #   Odds + Evens are different values
    # On the PERIMETER
    # We are cutting In / Out as manhattan top/left/right/bottom
    #     is all there is on a particular grid
    # -> Alternating Odd Even or Even/Odd based on step count
    #   E         (O)E(O)
    #  EOE       (O)EOE(O)  
    # EOEOE  -> (O)EOEOE(O)
    #  EOE       (O)EOE(O)
    #   E         (O)E(O)   
    
    #Calculate all distances from start to each possible location
    distances = self.calculate_distances()
    gr = self.width - self.start[0] -1 #(inside grid manhattan radius)

    #1. Calculate ODD /EVEN full count
    #print("ODDS", steps)
    oddcount = 0
    evencount = 0
    oddcorners = 0
    evencorners = 0
    for y in range(self.width):
      for x in range(self.width):
        if (x,y) in distances:
          v = distances[(x,y)]
          if v % 2 == 0:
            evencount += 1
            if v > gr:
              evencorners += 1
          else:
            oddcount += 1
            if v > gr:
              oddcorners += 1

    #2. Calculate EVEN full count
    print('Odds', oddcount, 'Evens', evencount)
    print('Odd Corners', oddcorners, 'Even Corners', evencorners)

    #total = 0
    #for n in distances:
    #  v = distances[n]
    #  if v == steps:
    #    total +=1
    #  elif v < steps and (v % 2 == 0):
    #    total +=1 
    #print("DEBUG TOTAL", total)

    #3. Calculate INSIDE manhatten of GRIDS (ODDS + EVENS) -> I (inclusive of perim)
    #print('x', x, 'w', self.width, 's', steps)
    #r = int(math.floor(self.width-x+steps / self.width)) + 1
    r = steps - gr
    r = (r / self.width) 
    print(r, 'Radius of GRIDS and', gr)
    if steps % 2 == 1:
      man_odd = (r+1)*(r+1)
      man_even = r*r
    else:
      man_odd = r*r
      man_even = (r+1)*(r+1)
    print('Man', man_odd, 'odd and', man_even, 'even')
    man_i = (man_odd * oddcount) + (man_even * evencount)

    #4. Calculate PERIM of manhatten GRIDS
    #5. cuts INTO PERIM (odd or even depending on start) -> C
    #6. cuts OUT of PERIM (odd or even depending on start) -> O

    man_in = (r+1)
    man_out = r
    print('In', man_in, 'Out', man_out)
    if steps % 2 == 1:
      man_o = man_out * evencorners
      man_c = man_in * oddcorners
    else:
      man_o = man_out * oddcorners
      man_c = man_in * evencorners

    #7. Total => I + O - C
    total = man_i + man_o - man_c
    print('Total', total)
    print()


  def result2_flood(self):
    steps = [6,10, 50, 100, 500, 1000, 5000]
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

import sys
import heapq

DELTAS = [
  (-1, 0),
  ( 1, 0),
  ( 0,-1),
  ( 0, 1)
]

CHANGE = {
  (1, 0): [(0,-1), (0,1)],
  (0, 1): [(-1,0), (1,0)],
  (-1,0): [(0,-1), (0,1)],
  (0,-1): [(-1,0), (1,0)]
}

MCHANGE = {
  'h': ('v', [(0,-1), (0,1)]),
  'v': ('h', [(-1,0), (1,0)]),
}

class Puzzle:

  def process(self, text):
    self.grid = []
    for line in text.split('\n'):
      self.process_line(line)

  def at(self, x, y):
    return self.grid[y][x]

  def moves(self, loc, d, mmin, mmax):
    moves = []
    newd, deltas = MCHANGE[d]
    x, y = loc
    for dx, dy in deltas:
      cost = 0
      #Calc cost to start of range
      for r in range(1,mmin):
        nx, ny = x+(r*dx), y+(r*dy)
        if nx >= 0 and ny >= 0 and nx < len(self.grid[0]) and ny < len(self.grid):
          cost += self.at(nx, ny)
        
      for r in range(mmin, mmax+1):
        nx, ny = x+(r*dx), y+(r*dy)
        if nx >= 0 and ny >= 0 and nx < len(self.grid[0]) and ny < len(self.grid):
          cost += self.at(nx, ny)
          moves.append(((nx, ny), cost, newd))

    return moves

  def neighbours(self, x, y):
    options = []
    for dx, dy in DELTAS:
      nx, ny = x+dx, y+dy
      if nx >= 0 and ny >= 0 and nx < len(self.grid[0]) and ny < len(self.grid):
        options.append(((nx, ny), (dx, dy)))
    return options

  def ultra_neighbours(self, loc, history):
    x, y = loc
    options = []
    #If we haven't gone 4 in same direction, we must continue
    if history == []:
      for dx, dy in DELTAS:
        nx, ny = x+dx, y+dy
        if nx >= 0 and ny >= 0 and nx < len(self.grid[0]) and ny < len(self.grid):
          options.append(((nx, ny), (dx, dy)))
    elif len(history) == 10:
      last = history[-1]
      same = True
      for h in history:
        same = same and (h == last)
      if same:
        #Must Change
        deltas = CHANGE[last]
        #print('Change', deltas)
        for dx, dy in deltas:
          nx, ny = x+dx, y+dy
          if nx >= 0 and ny >= 0 and nx < len(self.grid[0]) and ny < len(self.grid):
            options.append(((nx, ny), (dx, dy)))
      else:
        #IF last 4 same
        last4 = history[-4:]
        last = history[-1]
        same = True
        for h in last4:
          same = same and (h == last)
         
        #Continue
        dx, dy = last4[-1]
        nx, ny = x+dx, y+dy
        if nx >= 0 and ny >= 0 and nx < len(self.grid[0]) and ny < len(self.grid):
          options.append(((nx, ny), (dx, dy)))

        #Can Change
        if same and len(last4) == 4:
          deltas = CHANGE[last]
          for dx, dy in deltas:
            nx, ny = x+dx, y+dy
            if nx >= 0 and ny >= 0 and nx < len(self.grid[0]) and ny < len(self.grid):
              options.append(((nx, ny), (dx, dy)))
    else:
      if len(history) < 4:
        last4 = history
      else:
        last4 = history[-4:]

      last = history[-1]
      same = True
      for h in last4:
        same = same and (h == last)
       
      #Continue
      dx, dy = last4[-1]
      nx, ny = x+dx, y+dy
      if nx >= 0 and ny >= 0 and nx < len(self.grid[0]) and ny < len(self.grid):
        options.append(((nx, ny), (dx, dy)))

      #Can Change
      if same and len(last4) == 4:
        deltas = CHANGE[last]
        for dx, dy in deltas:
          nx, ny = x+dx, y+dy
          if nx >= 0 and ny >= 0 and nx < len(self.grid[0]) and ny < len(self.grid):
            options.append(((nx, ny), (dx, dy)))
    return options

  def process_line(self, line):
    if line != '':
      self.grid.append([int(n) for n in line])

  def a_h(self, loc, end):
    pass

  def a_star(self, start=(0,0)):
    #Infinity all cells
    g_score = {}
    f_score = {}

    for y in range(len(self.grid)):
      for x in range(len(self.grid[0])):
        g_score[(x,y)] = sys.maxsize
        f_score[(x,y)] = sys.maxsize
    g_score[start] = self.at(start[0], start[1])
    start_h = self.a_h(start, end)
    f_score[start] = start_h
    pq = []
    heapq.heapify(pq)
    heapq.heappush(pq, [(start_h, start_h), start])
    paths = {}
    found = False

  def wexplore(self, start, end):
    bests = {}
    paths = {}
    seen = {}
    #All are most expensive routes
    #for y in range(len(self.grid)):
    #  for x in range(len(self.grid[0])):
    #    nbrs = self.neighbours(x, y)
    #    for n, _ in nbrs:
    #      bests[((x, y), n)] = sys.maxsize

    last3 = ((-2, -2), (-2, -2), (-2, -2))
    floc = (-1, -1)
    bests[(start, last3)] = sys.maxsize
    toexplore = [(start, 0, last3, floc, [])]

    ebest = sys.maxsize
    ebest = 1165 #Dijkstra wrong
    n = 0

    while toexplore:
      n += 1
      if (n % 10000 == 0):
        print('Turn', n, 'still', len(toexplore), 'toexplore')
      loc, dist, last3, floc, path = toexplore.pop(0)
      #if (loc, last3) not in seen:
      #  seen[(loc, last3)] = True
    
      if (loc, last3) not in bests or bests[(loc, last3)] > dist:
        bests[(loc, last3)] = dist
        paths[(loc, last3)] = path + [loc]

        if(loc == end):
          print('Solution', dist)
          ebest = dist

        #print(loc, 'from', floc, 'for', dist)
        options = self.neighbours(loc[0], loc[1])
        for o, do in options:
          if last3[0] == last3[1] == last3[2] == do:
            #Does not change direction
            pass
          elif o != floc: #90deg turn required, no 180
            dd = self.at(o[0], o[1])
            if dist+dd < ebest: #Crop slower than one known solution
              nlast3 = (last3[1], last3[2], do)
              toexplore.append( (o, dist+dd, nlast3, loc, path + [loc]) )
    path = []
    mpath = sys.maxsize
    for loc, last3 in bests:
      if loc == end:
        if bests[(loc, last3)] < mpath:
          mpath = bests[(loc, last3)]
          path =  paths[(loc, last3)]
    return mpath, path


  def dijk(self, start, end):
    pq = []
    heapq.heapify(pq)
    path = [start]
    shortest = {}
    #Because you already start in the top-left block, you don't incur that block's heat loss unless you leave that block and then return to it.
    last3 = ((-2, -2), (-2, -2), (-2, -2))
    heapq.heappush(pq, [0, start,  path, last3, (-1, -1) ])

    best = None
    bdist = sys.maxsize

    while pq:
      dist, loc, journey, last3, floc = heapq.heappop(pq)
      #print(dist, loc, journey)
      if (loc, last3) not in shortest or shortest[(loc, last3)] > dist:
        shortest[(loc, last3)] = dist
        if loc == end:
          # print 'Solved', loc, dist
          if dist < bdist:
            best = journey
            bdist = dist
          #return dist, journey
        options = self.neighbours(loc[0], loc[1])
        for o, do in options:
          if last3[0] == last3[1] == last3[2] == do:
            #Does not change direction
            pass
          elif o != floc:
            nlast3 = (last3[1], last3[2], do)
            dd = self.at(o[0], o[1])
            heapq.heappush(pq, [dist+dd, o, journey + [o], nlast3, loc])
    return (bdist, best)

  def ultra_dijk(self, start, end):
    pq = []
    heapq.heapify(pq)
    path = [start]
    shortest = {}
    #Because you already start in the top-left block, you don't incur that block's heat loss unless you leave that block and then return to it.
    hist = []
    heapq.heappush(pq, [0, start,  path, hist, (-1, -1) ])

    best = None
    bdist = sys.maxsize

    while pq:
      dist, loc, journey, hist, floc = heapq.heappop(pq)
      #print(dist, loc, journey)
      thist = tuple(hist)
      if (loc, thist) not in shortest or shortest[(loc, thist)] > dist:
        shortest[(loc, thist)] = dist
        if loc == end:
          # print 'Solved', loc, dist
          if dist < bdist:
            best = journey
            bdist = dist
          #return dist, journey
        options = self.ultra_neighbours(loc, hist)
        for o, do in options:
          nhist = hist[-9:] + [do]
          dd = self.at(o[0], o[1])
          heapq.heappush(pq, [dist+dd, o, journey + [o], nhist, loc])
    return (bdist, best)

  def ultra_dijk2(self, start, end):
    pq = []
    heapq.heapify(pq)
    path = [start]
    shortest = {}
    hist = []
    starter = []
    #vmoves
    moves = self.moves((0, 0), 'v', 4, 10)
    for m in moves:
      heapq.heappush(pq, [m[1], m,  [m]])
    starter += moves
    #hmoves
    moves = self.moves((0, 0), 'h', 4, 10)
    for m in moves:
      heapq.heappush(pq, [m[1], m,  [m]])
    starter += moves

    best = None
    bdist = sys.maxsize

    while pq:
      dist, move, path = heapq.heappop(pq)
      loc, mdist, mdir = move
      if (loc, mdir) not in shortest or shortest[(loc, mdir)] > dist:
        shortest[(loc, mdir)] = dist
        if loc == end:
          #print('Solved', loc, dist)
          if dist < bdist:
            best = path
            bdist = dist
          #print(path)
          #return (dist, path)
        options = self.moves(loc, mdir, 4, 10)
        for o in options:
          dd = o[1]
          heapq.heappush(pq, [dist+dd, o, path + [o]])
    return (bdist, best)

  def result(self):
    self.result3()

  def result1(self):
    start = (0,0)
    end = (len(self.grid[0])-1, len(self.grid)-1)
    result = self.dijk(start, end)
    #result = self.wexplore(start, end)
    if(result != None):
      dist, path = result
      #print('PATH:', dist, path)
    else:
      print('Fail')
    self.dump_path(path)
    print('Path Length', dist)

  def result2(self):
    start = (0,0)
    end = (len(self.grid[0])-1, len(self.grid)-1)
    result = self.ultra_dijk(start, end)
    if(result != None):
      dist, path = result
      #print('PATH:', dist, path) else:
      print('Fail')
    self.dump_path(path)
    print('Path Length', dist)

  def result3(self):
    start = (0,0)
    end = (len(self.grid[0])-1, len(self.grid)-1)
    result = self.ultra_dijk2(start, end)
    if(result != None):
      dist, path = result
      #print('PATH:', dist, path)
    else:
      print('Fail')
    traced = []
    current = (0,0)
    cx, cy = current
    for loc, _, ddir in path:
      lx, ly = loc
      if ddir == 'h':
        dx = int((lx-cx) / abs(lx-cx))
        dy = 0
      else:
        dy = int((ly-cy) / abs(ly-cy))
        dx = 0
      #print('Trace', (cx, cy), '->', loc, 'with', (dx, dy))
      
      while((cx, cy) != loc):
        #print(cx, cy, dx, dy, '?', loc)
        traced.append((cx, cy))
        cx, cy = cx + dx, cy + dy
      traced.append(end)
      #print(loc, ddir)
    self.dump_path(traced)
    print('Path Length', dist)

  def dump_path(self, path):
    for y, r in enumerate(self.grid):
      for x, n in enumerate(self.grid[y]):
        if (x, y) in path:
          sys.stdout.write('*')
        else:
          sys.stdout.write(str(n))
      sys.stdout.write('\n')

if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

import sys
import heapq

DELTAS = [
  (-1, 0),
  ( 1, 0),
  ( 0,-1),
  ( 0, 1)
]

class Puzzle:

  def process(self, text):
    self.grid = []
    for line in text.split('\n'):
      self.process_line(line)

  def at(self, x, y):
    return self.grid[y][x]

  def neighbours(self, x, y):
    options = []
    for dx, dy in DELTAS:
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

  def result(self):
    self.result1()

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

import sys
from colorama import Fore
import heapq
from pyrsistent import pmap
from pyrsistent import pvector


"""
  Move -> 1 cost
  Turn -> 1000 cost (+/- 90)
"""

MOVES = {
  'E': (1, 0),
  'W': (-1,0),
  'N': (0,-1),
  'S': (0, 1),
}

NBRS = {
  'E': [((1, 0), 1   , 'E'), ((-1,0), 2001, 'W'), ((0,1), 1001, 'S'), ((0,-1), 1001, 'N')],
  'W': [((1, 0), 2001, 'E'), ((-1,0), 1,    'W'), ((0,1), 1001, 'S'), ((0,-1), 1001, 'N')],
  'N': [((1, 0), 1001, 'E'), ((-1,0), 1001, 'W'), ((0,1), 2001, 'S'), ((0,-1), 1,    'N')],
  'S': [((1, 0), 1001, 'E'), ((-1,0), 1001, 'W'), ((0,1), 1,    'S'), ((0,-1), 2001, 'N')],
}

OPPOSITE = {
  'N' : 'S',
  'S' : 'N',
  'E' : 'W',
  'W' : 'E'
}

TURNS = {
  'E': ['N', 'S'],
  'W': ['N', 'S'],
  'N': ['E', 'W'],
  'S': ['E', 'W']
}

class Puzzle:

  def process(self, text):
    self.maze = []
    for y, line in enumerate(text.split('\n')):
      self.process_line(line, y)
    self.width = len(self.maze[0])
    self.height = len(self.maze)

    self.graph_map()
    self.optimize_graph()


  def optimize_graph(self):
    hashgraph = {}

    for key in self.graph:
      hashgraph[key] = []
      for value in self.graph[key]:
        hashgraph[key].append( (value, []) )


    """
      walk graph (not backtracking) until there are
      a) no way to walk [DEAD END]
      b) >1 moves I can make

      if a) can cull UNLESS AT END!
      if b) can optimize to go Node -> That Node
        Add all walked nodes into set of tiles skipped
    """
    
    didoptimise = True
    while didoptimise:
      didoptimise = False
      for node in hashgraph:
        points = hashgraph[node]
        #Single moves can be culled
        if len(points) == 1:
          print(node, 'can be optimised')
          point = points[0]
          (cst, loc, d), tiles = point
          #go strait to loc's nodes
          directs = hashgraph[(loc, d)]
          print('>', directs)
          newpath = []
          #([(1, (1, 13), 'W'), (2001, (3, 13), 'E')], [])
          for (n, tiles) in directs:
            ncost, nloc, ndir = n
            if (nloc, ndir) == node:
              pass
            else:
              newpath.append( ((cst + ncost, nloc, ndir), tiles + [loc]) )
          print('=', newpath)
          hashgraph[node] = newpath
          didoptimize = True

        #Corridor walks can be culled 
        # (go in same direction until we hit a junction)

        #Deadends that are not E can be culled
        # (if traverse corridor until empty moves)
    
  
  def graph_map(self):
    visited = {}

    tovisit = [self.location]

    graph = {} #(loc, D) => [(cost, loc, D, tiles), (cost, loc, D, tiles)...]

    while tovisit:
      current = tovisit.pop()
      loc, direction = current


      if (loc, direction) not in graph:
        graph[(loc, direction)] = set()

      #print ('Visiting:', loc, direction)
      if (loc, direction) not in visited:
        visited[(loc, direction)] = True

        #Either can go in direction, or turn
        options = NBRS[direction]
        for (dx, dy), cst, nd in options:
          nx, ny = loc[0] + dx, loc[1]+dy
          nloc = (nx, ny)
          newnode = (nloc, nd)
          if self.at(nx, ny) != '#':
            #print('Add', loc, direction, '->', loc, turn)
            graph[(loc, direction)].add( (cst, (nx, ny), nd) )

            if newnode not in visited:
              tovisit.append( newnode )


    print('Graph Built!')
    self.graph = graph


  def at(self, x, y):
    return self.maze[y][x]

  def find_all_best_paths(self):
    raise 'Sort the path to be tiles visited or skipped'
    bestlen = None
    bests = []
    tovisit = []
    heapq.heapify(tovisit)
    #heapq.heappush(tovisit, (0, self.location, [], set(), set()))
    visited = pmap()
    heapq.heappush(tovisit, (0, self.location, [], visited))

    while tovisit:
      current = heapq.heappop(tovisit)
      cost, (loc, direction), path, visited = current

      if (bestlen and cost <= bestlen) or (bestlen == None):
        #print('Visiting:', cost, loc, direction)
        if loc == self.end:
          print('Found A Path!', cost)
          bests.append(path + [(loc, direction, cost)])
          bestlen = cost

        if (loc, direction) not in visited:
          for node in self.graph[(loc, direction)]:
            ncost, nloc, ndirection = node
            if (nloc, ndirection) not in visited:
              heapq.heappush(tovisit, (cost+ncost, \
                (nloc, ndirection), \
                path + [(loc, direction, cost)], \
                visited.set((loc, direction), True),
                ))


    return bests

  def x_find_all_best_paths(self):
    bestlen = None
    bests = []
    tovisit = []
    heapq.heapify(tovisit)
    #heapq.heappush(tovisit, (0, self.location, [], set(), set()))
    visited = pmap()
    visited2 = pmap()
    heapq.heappush(tovisit, (0, self.location, [], visited, visited2))

    while tovisit:
      current = heapq.heappop(tovisit)
      cost, (loc, direction), path, visited, visited2 = current

      if (bestlen and cost <= bestlen) or (bestlen == None):
        #print('Visiting:', cost, loc, direction)
        if loc == self.end:
          print('Found A Path!', cost)
          bests.append(path + [(loc, direction, cost)])
          bestlen = cost

        for turn in TURNS[direction]:
          if (loc, turn) not in visited2:
            #nvisited[loc] = True
            #nvisited2[(loc, direction)] = True

            heapq.heappush(tovisit, (cost+1000, \
              (loc, turn), \
              path + [(loc, direction, cost)], \
              visited.set(loc, True),
              visited2.set((loc, direction), True)
              ))

        dx, dy = MOVES[direction]
        nx, ny = loc[0] + dx, loc[1] + dy
        if self.at(nx, ny) != '#' and (nx,ny) not in visited:
          heapq.heappush(tovisit, (cost+1, \
            ((nx, ny), direction), \
            path + [(loc, direction, cost)], 
            visited.set(loc, True),
            visited2.set((loc, direction), True)
            ))

    return bests


  def find_path(self):
    tovisit = []
    heapq.heapify(tovisit)
    #visited = {}
    #visited2 = {}

    visited = pmap()
    visited2 = pmap()

    #visited = pvector()
    #visited2 = pvector()

    #print(tovisit)
    heapq.heappush(tovisit, (0, self.location, []))

    while tovisit:
      current = heapq.heappop(tovisit)
      cost, (loc, direction), path = current
      #print('Visiting:', cost, loc, direction)
      if loc == self.end:
        return path + [(loc, direction, cost)]

      #visited[loc] = True
      #visited2[(loc, direction)] = True
      visited = visited.set(loc, True)
      visited2 = visited.set((loc, direction), True)
      #visited = visited.append(loc)
      #visited2 = visited.append((loc, direction))

      for turn in TURNS[direction]:
        if (loc, turn) not in visited2:
          heapq.heappush(tovisit, (cost+1000, (loc, turn), path + [(loc, direction, cost)]))

      dx, dy = MOVES[direction]
      nx, ny = loc[0] + dx, loc[1] + dy
      if self.at(nx, ny) != '#' and (nx,ny) not in visited:
        heapq.heappush(tovisit, (cost+1, ((nx, ny), direction), path + [(loc, direction, cost)]))

  def process_line(self, line, y):
    if line != '':
      for x, ch in enumerate(line):
        if ch == 'S':
          self.location = ((x, y), 'E')
        elif ch == 'E':
          self.end = (x,y)
      self.maze.append(line)

  def result(self):
    self.result2()

  def result2(self):
    paths = self.find_all_best_paths()
    locs = set()
    print(len(paths))
    for path in paths:
      for loc, _, _ in path:
        locs.add(loc)
    print(list(locs))
    print('Total Spots:', len(locs))

  def result1(self):
    path = self.find_path()
    print(path)
    last = path[-1]
    cost = last[2]
    print('Total Cost:', cost)


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

import sys
from colorama import Fore
import heapq
from pyrsistent import pmap
from pyrsistent import pvector
from collections import defaultdict


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
    self.debug_graph(self.graph)

    self.optimize_graph()
    self.debug_graph(self.graph)

  def debug_graph(self, graph):
    points = {}
    for node in graph:
      loc, _ = node
      count = points.get(loc, 0)
      count += 1
      points[loc] = count

    for y in range(self.height):
      for x in range(self.width):
        if self.maze[y][x] == '#':
          print(Fore.RED + '#' + Fore.RESET, end='')
        elif self.maze[y][x] == '.':
          if (x,y) in points:
            print(Fore.CYAN + str(points[(x,y)]) +  Fore.RESET, end='')
          else:
            print('.', end='')
        else:
          print(Fore.GREEN + self.maze[y][x] + Fore.RESET, end='')
      print('')
          
  def debug_path(self, path):
    points = {}
    for loc in path:
      points[loc] = True

    for y in range(self.height):
      for x in range(self.width):
        if self.maze[y][x] == '#':
          print(Fore.RED + '#' + Fore.RESET, end='')
        elif self.maze[y][x] == '.':
          if (x,y) in points:
            print(Fore.CYAN + '*' +  Fore.RESET, end='')
          else:
            print('.', end='')
        else:
          print(Fore.GREEN + self.maze[y][x] + Fore.RESET, end='')
      print('')


  def find_junction(self, node, fromnode, graph, nest=''):
    #node:
    # ((1, (2, 13), 'E'), [])
    # ((cost, loc, direction), tilesskipped) 

    (cost, loc, direction), skipped = node
    #print('Finding A Junction', loc, direction, 'from', fromnode)

    curloc, curdirection = loc, direction
    fromloc = fromnode[0]

    if self.at(curloc[0], curloc[1]) == 'E' or \
       self.at(curloc[0], curloc[1]) == 'S':
      #Consider a Junction
      return node

    options = graph[(curloc, curdirection)]
    togoto = []
    #print(nest, loc, 'from', fromnode, '>', options)
    for option in options:
      #((2001, (1, 13), 'W'), [])
      (_, oloc, _), _ = option
      if oloc != fromloc:
        togoto.append(option) 
    #print(nest, '==>', togoto)
    
    if len(togoto) == 1: #Corridor
      #print(nest + str(loc))
      #BUG, recursive node is not (loc, direction)
      jnode = self.find_junction(togoto[0], (loc, direction), graph, nest+' ')
      if jnode:
        (jcost, jloc, jdirection), jskipped = jnode
        newnode = ((cost + jcost, jloc, jdirection), skipped + jskipped + [loc])
        return newnode
      else:
        return None
    elif len(togoto) == 0:
      return None
    else:
      #At A Junction!
      return node

  def optimize_graph(self):
    """
      walk graph (not backtracking) until there are
      a) no way to walk [DEAD END]
      b) >1 moves I can make

      if a) can cull UNLESS AT END!
      if b) can optimize to go Node -> That Node
        Add all walked nodes into set of tiles skipped
    """
    
    newgraph = {}

    visited = {}
    tovisit = [self.location]
    while tovisit:
      current = tovisit.pop()
      loc, direction = current
      if current not in visited:
        visited[current] = True
        options = self.graph[(loc, direction)]
        newgraph[current] = []
        newoptions = []
        for option in options:
          #print(loc, '-->', option, 'from', current, '?')
          junction = self.find_junction(option, current, self.graph)
          if junction:
            #((2003, (2, 13), 'W'), [(2, 13)])
            (_, jloc, jdir), _ = junction
            newgraph[current].append(junction)
            tovisit.append( (jloc, jdir) )
          else:
            #print('Deadend Nixed')
            pass

    self.graph = newgraph
    print('Graph Optimized!', len(newgraph.keys()), 'nodes')
  
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


    print('Graph Built!', len(graph.keys()), 'nodes')

    hashgraph = {}

    for key in graph:
      hashgraph[key] = []
      for value in graph[key]:
        hashgraph[key].append( (value, []) )


    self.graph = hashgraph


  def at(self, x, y):
    return self.maze[y][x]

  def find_all_best_paths(self):
    bestlen = 73432
    bests = []
    tovisit = []
    heapq.heapify(tovisit)

    visited = {}
    heapq.heappush(tovisit, (0, self.location, [], visited))

    while tovisit:
      current = heapq.heappop(tovisit)
      #(0, ((1, 13), 'E'), [], pmap({}))
      #print(current)
      cost, (loc, direction), tiles, visited = current

      if (bestlen and cost <= bestlen) or (bestlen == None):
        #print('Visiting:', cost, loc, direction)
        if loc == self.end:
          print('Found A Path!', cost)
          bests.append(tiles + [loc])
          bestlen = cost
        elif loc not in visited:
          for node in self.graph[(loc, direction)]:
            #node: ((2003, (2, 13), 'W'), [(2, 13)])
            (ncost, nloc, ndirection), ntiles = node
            if nloc not in visited:

              nvisited = visited.copy()
              nvisited[loc] = True

              heapq.heappush(tovisit, (cost+ncost, \
                (nloc, ndirection), \
                tiles + [loc] + ntiles, \
                #visited.set((loc, direction), True),
                #visited | set([loc])
                nvisited
                ))

    return bests


  def find_graph_path_all(self):
    tovisit = []

    costs = {node: float('inf') for node in self.graph}

    costs[(self.end, 'E')] = float('inf')
    costs[(self.end, 'N')] = float('inf')

    costs[self.location] = 0

    paths = defaultdict(list)
    paths[self.location].append([self.location[0]])

    heapq.heappush(tovisit, (0, self.location))

    while tovisit:
      cost, current = heapq.heappop(tovisit)
      if cost > costs[current]:
        continue

      options = self.graph[current]
      for option in options:
        #option: [((1002, (1, 11), 'N'), [(1, 12)])]
        (ocost, oloc, odirection), oskipped = option
        oncost = cost + ocost
        onode = (oloc, odirection)

        if oncost < costs[onode]:
          costs[onode] = oncost
          paths[onode] = [path + oskipped + [oloc] for path in paths[current]]
          heapq.heappush(tovisit, (oncost, onode) )
        elif oncost == costs[onode]:
          paths[onode].extend( path + oskipped + [oloc] for path in paths[current] )

    
    #Shortest paths to both type of end (coming in east, coming in north)
    # in top corner so cannot comin travelling W or S
    if costs[(self.end, 'N')] < costs[(self.end, 'E')]:
      return paths[(self.end,'N')], costs[(self.end, 'N')]
    elif costs[(self.end, 'N')] > costs[(self.end, 'E')]:
      return paths[(self.end,'E')], costs[(self.end, 'E')]
    else:
      return paths[(self.end,'E')] + paths[(self.end, 'N')],\
        costs[(self.end, 'E')]

  def find_graph_path_all_x(self):
    tovisit = []
    heapq.heapify(tovisit)

    #visited = {}
    visited = {}

    #print(tovisit)
    heapq.heappush(tovisit, (0, self.location, [], visited))
    #tovisit.append( (0, self.location, [], visited) )

    while tovisit:
      current = heapq.heappop(tovisit)
      #current = tovisit.pop()
      cost, (loc, direction), path, visited = current
      #print('Visiting:', cost, loc, direction)
      if loc == self.end:
        print('tv:', len(tovisit))
        return path + [loc]
    
      if len(tovisit) % 250000 == 0:
        print('tv:', len(tovisit), 'c:', cost)

      if loc not in visited:
        options = self.graph[(loc, direction)]
        for option in options:
          #option: [((1002, (1, 11), 'N'), [(1, 12)])]
          (ocost, oloc, odirection), oskipped = option
          if oloc not in visited:
            nvisited = visited.copy()
            nvisited[loc] = True
            heapq.heappush(tovisit, \
            #tovisit.append( \
              (
                cost+ocost, \
                (oloc, odirection), \
                path + oskipped + [loc],
                nvisited
              )
            )

  def find_graph_path(self):
    tovisit = []
    heapq.heapify(tovisit)
    #visited = {}
    visited = set()
    #print(tovisit)
    heapq.heappush(tovisit, (0, self.location, []))

    while tovisit:
      current = heapq.heappop(tovisit)
      cost, (loc, direction), path = current
      #print('Visiting:', cost, loc, direction)
      if loc == self.end:
        return path + [loc]

      if loc not in visited:
        #visited[loc] = True
        visited = visited | set([loc])
        options = self.graph[(loc, direction)]
        for option in options:
          #option: [((1002, (1, 11), 'N'), [(1, 12)])]
          (ocost, oloc, odirection), oskipped = option
          heapq.heappush(tovisit, \
            (
              cost+ocost, (oloc, odirection), \
              path + oskipped + [loc]
            )
          )


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
    #for node in self.graph:
    #  print(node, self.graph[node])
    #self.result_graph()

  def result2(self):
    #paths = self.find_all_best_paths()
    paths, cost = self.find_graph_path_all()
    print('Number of Paths:', len(paths))
    locs = set()
    for i, path in enumerate(paths):
      #print('>', len(path), 'costs', cost)
      for loc in path:
        locs.add(loc)
    self.debug_path(locs)
    print('Total Spots:', len(locs))

  def result1(self):
    path = self.find_path()
    print(path)
    last = path[-1]
    cost = last[2]
    print('Total Cost:', cost)

  def result_graph(self):
    pass
    #path = self.find_graph_path_all()
    #print('Total Tiles:', len(path))
    #self.debug_path(path)

if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

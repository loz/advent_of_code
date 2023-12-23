import sys
import heapq

DELTAS = [
  (-1,0), (1,0), (0,-1), (0,1)
]

SLOPE = {
  'v': (0,1),
  '>': (1,0),
  '^': (0,-1),
  '<': (-1,0),
}

class Puzzle:

  def process(self, text):
    self.map = {}
    for y, line in enumerate(text.split('\n')):
      self.process_line(line, y)
    self.height = y
    #print('Size', self.width, self.height)

  def at(self, loc):
    return self.map.get(loc, '#')

  def process_line(self, line, y):
    if line != '':
      for x, ch in enumerate(line):
        self.map[(x, y)] = ch
      self.width = x+1

  def dump_path(self, path):
    #start = (1,0)
    #end=(self.width-2, self.height-1)
    for y in range(self.height):
      for x in range(self.width):
        #if (x,y) == start:
        #  sys.stdout.write(u"\u001b[33mS")
        #elif (x,y) == end:
        # sys.stdout.write(u"\u001b[33mE")
        #elif (x,y) in path:
        if (x,y) in path:
          sys.stdout.write(u"\u001b[32mO")
        else:
          ch = self.at((x,y))
          if ch == '#':
            sys.stdout.write(u"\u001b[33m#")
          else:
            sys.stdout.write(u"\u001b[0m"+ch)
      sys.stdout.write('\n')
    sys.stdout.write(u"\u001b[0m\n")

  def longest(self):
    start = (1,0)
    end=(self.width-2, self.height-1)
    first = (1,1) #can ignore out of bounds if start on first accessible
    seen = {start}
    tovisit = [(first, [start], seen)]
    ends = []
    while(tovisit):
      loc, path, seen = tovisit.pop(0)
      #print('Visiting', loc, len(path))
      x, y = loc
      ch = self.at(loc)
      if ch in "v>^<":
        deltas = [SLOPE[ch]]
      else:
        deltas = DELTAS
      for dx, dy in deltas:
        nx, ny = x + dx, y+dy
        if (nx, ny) == end:
          ends.append(path + [loc, (nx,ny)])
        elif self.at((nx, ny)) != '#':
          if (nx,ny) not in seen:
            #print('N', (nx, ny), self.width, 'x', self.height)
            tovisit.append( ((nx, ny), path + [loc], seen | {loc} ) )
    #print("="*80)
    longest = ends[0]
    for e in ends:
      if len(e) > len(longest):
        longest = e
      #print(len(e), '>>', e)
    #print("="*80)
    #print(longest)
    #print("="*80)
    return longest

  def longest_no_slopes(self):
    start = (1,0)
    end=(self.width-2, self.height-1)
    first = (1,1) #can ignore out of bounds if start on first accessible
    seen = dict({start:True})
    tovisit = [(first, [start], seen)]
    ends = []
    while(tovisit):
      loc, path, seen = tovisit.pop(0)
      #print('Visiting', loc, len(path))
      x, y = loc
      deltas = DELTAS
      for dx, dy in deltas:
        nx, ny = x + dx, y+dy
        if (nx, ny) == end:
          ends.append(path + [loc, (nx,ny)])
        elif self.map[ny][nx] != '#':
          if (nx,ny) not in seen:
            nseen = dict(seen)
            nseen[(nx, ny)] = True
            tovisit.append( ((nx, ny), path + [loc], nseen) )
    longest = ends[0]
    for e in ends:
      if len(e) > len(longest):
        longest = e
    return longest

  def longest_no_slopes_dijk(self):
    #Use NEGATIVE distances for SHORTEST PATH
    start = (1,0)
    end=(self.width-2, self.height-1)
    first = (1,1) #can ignore out of bounds if start on first accessible
    seen = {start:True}
    tovisit =  []
    heapq.heapify(tovisit)
    heapq.heappush(tovisit, [0, first, [start]])
    longest = []
    while(tovisit):
      distance, loc, path = tovisit.pop(0)
      #print('Visiting', loc, len(path))
      x, y = loc
      deltas = DELTAS
      for dx, dy in deltas:
        nx, ny = x + dx, y+dy
        if (nx, ny) == end:
          #ends.append(path + [loc, (nx,ny)])
          new = path + [loc, (nx,ny)]
          if len(new) > len(longest):
            longest = new
          #break
        elif self.map[ny][nx] != '#':
          if (nx,ny) not in seen:
            seen[(nx,ny)] = True
            #print('N', (nx, ny), self.width, 'x', self.height)
            #tovisit.append( ((nx, ny), path + [loc], seen | {loc} ) )
            heapq.heappush(tovisit, [distance-1, (nx,ny), path + [loc]] )
    return longest

  def condense_map(self):
    start = (1,0)
    end=(self.width-2, self.height-1)
    nodes = {(start):True}
    vertices = {start:{}}
    tovisit = []
    tovisit.append((start, start, start, 0))
    seen = {start:True}
    while(tovisit):
      loc, lastnode, lastbox, distance = tovisit.pop(0)
      x, y = loc
      deltas = DELTAS
      nexts = [(x+dx, y+dy) for dx, dy in deltas]
      nexts = [n for n in nexts if n != lastbox ]
      nexts = [n for n in nexts if self.at(n) != '#']
      if len(nexts) > 1 or loc == end:
        #Node
        if loc not in nodes:
          nodes[loc] = True
          vertices[loc] = {lastnode: distance}
          vertices[lastnode][loc] = distance
          for n in nexts:
            tovisit.append( (n, loc, loc, 1) )
        else:
          #Mark the vertex
          vertices[loc][lastnode] = distance
          vertices[lastnode][loc] = distance
          pass
      elif nexts:
        n = nexts[0]
        tovisit.append( (n, lastnode, loc, distance+1) )
    #print(nodes)
    #print(vertices)
    points = nodes.keys()
    return vertices
    #self.dump_path(points)

  def unvisited(self, graph, visited):
    seen = {}
    for k in graph:
      nodes = graph[k]
      for o in nodes:
        if k in visited and o in visited:
          pass
        else:
          if (k, o) not in seen and (o,k) not in seen:
            seen[(k,o)] = nodes[o]
    return sum(seen.values())

  def longest_graph(self, graph):
    start = (1,0)
    end=(self.width-2, self.height-1)
    visited = {start:True}
    tovisit = [(start, 0, visited )]
    longest = 0
    print('Max possible', self.unvisited(graph, []))
    while(tovisit):
      loc, distance, visited = tovisit.pop()
      if loc == end:
        if distance > longest:
          longest = distance
          print('New Longest', distance)
      else:
        nodes = graph[loc]
        #Can I prune if remining vertex lengths < longest so far?
        unvisited = self.unvisited(graph, visited.keys())
        if distance + unvisited < longest:
          #print('Pruning')
          pass
        else:
          for n in nodes:
            d = nodes[n]
            if n not in visited:
              nvisited = dict(visited)
              nvisited[n] = True
              #print(loc, '->', n, '=', d)
              tovisit.append( (n, distance+d, nvisited) )
    return longest

  def longest_grapha(self, graph):
    start = (1,0)
    end=(self.width-2, self.height-1)
    #Sort Graph
    def top_sort(graph):
      visited = {}
      stack = []
      
      def dfs(node):
        if node not in visited:
          visited[node] = True
          for nk in graph[node]:
            dfs(nk)
          stack.append(node)

      for v in graph:
        dfs(v)

      return stack[::-1] #Reverse

    sgraph = top_sort(graph)
    #print(sgraph)
    
    #Initialise with smallest distances
    distances = {}
    for v in graph:
      distances[v] = -1 * sys.maxsize
    distances[start] = 0

    #print(distances)
    #Update distances
    for v in sgraph:
      nbrs = graph[v]
      for n in nbrs:
        d = nbrs[n]
        if distances[v] + d > distances[n]:
          distances[n] = distances[v] + d 

    print(distances)
    return distances[end]

  def result(self):
    self.result2()

  def result1(self):
    longest = self.longest()
    self.dump_path(longest)
    print('Path', len(longest)-1)

  def result2(self):
    graph = self.condense_map()
    self.dump_path(graph.keys())
    print("Nodes", len(graph.keys()))
    longest = self.longest_graph(graph)
    print("Longest", longest)

if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

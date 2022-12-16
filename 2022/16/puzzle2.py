import sys
import re
import heapq
import itertools
import math

class Puzzle:

  def process(self, text):
    self.start = ('AA', set())
    self.valves = {}

    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      data = re.match('Valve (.+) has flow rate=(.+); tunnels* leads* to valves* (.+)', line)
      parts = data.groups()
      valve = parts[0]
      flow = int(parts[1])
      exits = parts[2].split(', ')
      self.valves[valve] = (flow, exits)

  def options(self, state):
    options = []
    idx, onlist = state
    flow, exits = self.valves[idx]
    if flow != 0 and idx not in onlist:
      cpy = onlist.copy()
      cpy.add(idx)
      options.append((idx, cpy))
    for exit in exits:
      options.append((exit, onlist.copy()))
    return options
  
  def traverse(self, graph, curnode, timer, visited, maxtimer=30):
    paths = []
    for node in graph[curnode].keys():
      if node not in visited:
        ndist = graph[curnode][node]
        if timer + ndist + 1 < maxtimer:
          paths += self.traverse(graph, node, timer+ndist+1, visited + [curnode])
    paths.append(visited + [curnode])
    return paths

  def result1(self):
    relevant = []
    for v in self.valves.keys():
      if self.valves[v][0] != 0:
        relevant.append(v)

    newgraph = {}
    for node in ['AA'] + relevant:
      distances = {}
      for other in ['AA'] + relevant:
        if node != other:
          distances[other] = self.shortest_path(node, other)
      newgraph[node] = distances

    paths = self.traverse(newgraph, 'AA', 0, [])
    largestpath = []
    largest = 0
    for path in paths:
      t = 0
      flow = 0
      released = 0
      nodes = list(path)
      curnode = nodes.pop(0)
      while nodes:
        nextnode = nodes.pop(0)
        dist = newgraph[curnode][nextnode]
        curnode = nextnode
        if t+dist >= 30:
          continue
        released += (flow * dist) + flow
        flow += self.valves[curnode][0]
        t += dist + 1
      if t < 30:
        released += ((30-t) * flow)
        t = 30
      #print 'AA ->', path, flow, released, t
      if largest < released:
        largest = released
        largestpath = path
    print 'Largest', largest
    print 'Path', largestpath

  def calculate_flow(self, path, newgraph, maxtimer):
    t = 0
    flow = 0
    released = 0
    nodes = list(path)
    curnode = nodes.pop(0)
    while nodes:
      nextnode = nodes.pop(0)
      dist = newgraph[curnode][nextnode]
      curnode = nextnode
      if t+dist >= maxtimer:
        continue
      released += (flow * dist) + flow
      flow += self.valves[curnode][0]
      t += dist + 1
    if t < maxtimer:
      released += ((maxtimer-t) * flow)
    return released
    

  def result(self):
    print 'Calculating Relevant'
    relevant = []
    for v in self.valves.keys():
      if self.valves[v][0] != 0:
        relevant.append(v)
  
    print 'Graphing Nodes'
    newgraph = {}
    for node in ['AA'] + relevant:
      distances = {}
      for other in ['AA'] + relevant:
        if node != other:
          distances[other] = self.shortest_path(node, other)
      newgraph[node] = distances

    print 'Traversing For Candidates'
    paths = self.traverse(newgraph, 'AA', 0, [], 26)

    print 'Calculating Results'
    cache = {}
    for path in paths:
      pk = ''.join(path)
      cache[pk] = self.calculate_flow(path, newgraph, 26)

    #Cheating?  is a 50/50 split reasonable?
    paths = filter(lambda x: len(x) <= (len(relevant)/2)+1, paths)

    print 'Sorting Paths'
    paths.sort(key=lambda x: cache[''.join(x)], reverse=True)

    for path in paths:
      print path, '=>', cache[''.join(path)]

    #return
    pairs = itertools.combinations(paths, 2)
    print 'Finding Pairs'
    n = len(paths)
    print (n*(n-1))/2, 'Potential Pairs'
    largestpath = []
    largest = 0
    for pair in pairs:
      p1, p2 = pair
      p1 = set(p1)
      p2 = set(p2)
      if set(p1).intersection(set(p2)) == set(['AA']):
        mk = ''.join(pair[0])
        ek = ''.join(pair[1])
        my_val = cache[mk]
        el_val = cache[ek]
        if largest < my_val + el_val:
          largest = my_val + el_val
          largestpath = pair
          print 'NewLargest', pair, my_val, el_val, '=>', largest
    print 'Largest', largest
    print 'Path', largestpath

  def shortest_path(self, start, end):
    pq = []
    heapq.heapify(pq)
    distances = {}
    heapq.heappush(pq, (0, start))
    while pq:
      dist, node = heapq.heappop(pq)
      if node in distances.keys(): #is this better?
        if dist > distances[node]:
          continue
      distances[node] = dist
      exits = self.valves[node][1]
      for exit in exits:
        if exit in distances.keys():
          if (dist+1) < distances[exit]:
            heapq.heappush(pq, (dist+1, exit))
        else:
            heapq.heappush(pq, (dist+1, exit))
    return distances[end]

if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

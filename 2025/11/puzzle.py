import sys
from colorama import Fore

class Puzzle:

  def __init__(self):
    self.graph = {}

  def process(self, text):
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      left, right = line.split(': ')
      outs = right.split(' ')
      self.graph[left] = outs

  def count_targets(self, graph, dest, target='out'):
    total = 0
    if dest == target:
      return 1
    else:
      if dest not in graph:
        return 0
      nodes = graph[dest]
      for node in nodes:
        total += self.count_targets(graph, node, target)
    return total

  def can_reach(self, target, terminate=None, visited=[]):
    graph = {}
    nodes = []
    if target in visited:
      return graph
    for node in self.graph:
      if target in self.graph[node]:
        nodes.append(node)
    graph[target] = nodes
    if not terminate in nodes:
      for node in nodes:
        g = self.can_reach(node, terminate, visted + [target])
        for n in g:
          graph[n] = g[n]
    return graph

  def dfs_all(self, graph, start):
    visited = {}
    tovisit = [start]
    while tovisit:
      cur = tovisit.pop()
      visited[cur] = True
      if cur in graph:
        nodes = graph[cur]
        for node in nodes:
          if node not in visited:
            tovisit.append(node)
    return list(visited)


  def reverse_graph(self,graph):
    rgraph = {}
    for node in graph:
      for rnode in graph[node]:
        if rnode not in rgraph:
          rgraph[rnode] = []
        rgraph[rnode].append(node)
    return rgraph


  def render_dot(self, graph):
    print('digraph G {')
    for node in graph:
      print(node, '-> {', ' '.join(graph[node]), '}')
    print('}')

  def result1(self):
    count = self.count_targets('you')
    print('Paths:', count)

  def filter_graph(self, graph, includes):
    fgraph = {}
    for node in graph:
      if node in includes:
        fnodes = []
        for n in graph[node]:
          if n in includes:
            fnodes.append(n)
        fgraph[node] = fnodes
    return fgraph

  def result(self):
    start = 'svr'
    end = 'out'
    i1 = 'fft'
    i2 = 'dac'
    rgraph = self.reverse_graph(self.graph)
    can_reach_i1 = self.dfs_all(rgraph, i1)
    can_reach_i2 = self.dfs_all(rgraph, i2)
    i1_can_reach = self.dfs_all(self.graph, i1)
    i2_can_reach = self.dfs_all(self.graph, i2)
    
    s1 = set(can_reach_i1 + i1_can_reach)
    s2 = set(can_reach_i2 + i2_can_reach)
    nodes = s1 & s2
    fgraph = self.filter_graph(self.graph, nodes)

    #self.render_dot(fgraph)
    s_i1 = self.count_targets(fgraph, start, i1)
    i1_i2 = self.count_targets(fgraph, i1, i2)
    i2_e = self.count_targets(fgraph, i2, end)
    print(s_i1, i1_i2, i2_e)
    print('Total:', s_i1 * i1_i2 * i2_e)
    

if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

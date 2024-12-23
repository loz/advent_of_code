import sys
from colorama import Fore
from functools import cache
from itertools import combinations


"""
  EXAMPLE:
kh ['tc', 'qp', 'ub', 'ta']
tc ['kh', 'wh', 'td', 'co']
qp ['kh', 'ub', 'td', 'wh']
ub ['qp', 'kh', 'wq', 'vc']
ta ['co', 'ka', 'de', 'kh']

de ['cg', 'co', 'ta', 'ka']
cg ['de', 'tb', 'yn', 'aq']
ka ['co', 'tb', 'ta', 'de']
co ['ka', 'ta', 'de', 'tc']
yn ['aq', 'cg', 'wh', 'td']
aq ['yn', 'vc', 'cg', 'wq']
tb ['cg', 'ka', 'wq', 'vc']
vc ['aq', 'ub', 'wq', 'tb']
wh ['tc', 'td', 'yn', 'qp']
td ['tc', 'wh', 'qp', 'yn']
wq ['tb', 'ub', 'aq', 'vc']

[kh, 'tc', 'qp', 'ub', 'ta'] &&
  ['kh', 'wh', 'td', 'co'] &&
  ['kh', 'ub', 'td', 'wh'] &&
  ['qp', 'kh', 'wq', 'vc'] &&
  ['co', 'ka', 'de', 'kh'] 


"""
class Puzzle:

  def process(self, text):
    self.network ={}  
    for line in text.split('\n'):
      self.process_line(line)

  def nodes(self, source):
    return self.network[source]

  def process_line(self, line):
    if line != '':
      left, right = line.split('-')
      self.link_nodes(left, right)
      self.link_nodes(right, left)

  def link_nodes(self, left, right):
      if left not in self.network:
        self.network[left] = []
      self.network[left].append(right)

  def find_trios(self):
    cliques = self.bron_kerbosch()
    trios = []
    for c in cliques:
      if len(c) == 3:
        trios.append(c)
    return trios

  def find_trios_part1(self):
    trios = []
    seen = {}
    for a in self.network:
      nodes = self.network[a]
      for b in nodes:
        bnodes = self.network[b]
        for c in bnodes:
          if c != a:
            if c in bnodes and a in bnodes and \
               c in nodes:
              trio = [a, b, c]
              trio = sorted(trio)
              trio = set(trio)
              if tuple(trio) not in seen:
                seen[tuple(trio)] = True
                trios.append(trio)
    return trios

  def stringify(self, result):
    answer = sorted(result)
    answer = ','.join(answer)
    return answer
  
  def _r_bron_kerbosch(self, r, p, x, depth=''):
    if not p and not x:
      return [r]

    cliques = []
    for v in list(p):
      vnodes = set(self.network[v])
      nr = r | {v}
      np = p & vnodes
      nx = x & vnodes

      cliques.extend(self._r_bron_kerbosch(nr, np, nx, depth+' '))
      p.remove(v)
      x.add(v)
    return cliques

  def bron_kerbosch(self):
    r = set()
    p = set(self.network.keys())
    x = set()
    return self._r_bron_kerbosch(r, p, x)

  def result2(self):
    cliques = self.bron_kerbosch()
    best = None
    bestlen = 0
    for c in cliques:
      if len(c) > bestlen:
        best = c
        bestlen = len(c)
    print('Best', best)
    print('Password: ', self.stringify(best))

  def result2_slow(self):
    connecteds = []
    for node in self.network:
      print('.', end='', flush=True)
      connected = self.sets_of_connected(node) 
      for connections in connected:
        if connections not in connecteds:
          connecteds.append(connections)
    best = connecteds[0]
    bestlen = len(best)
    for connection in connecteds:
      if len(connection) > bestlen:
        best = connection
        bestlen = len(best)
    print()
    print('Largest:', best, len(best))
    answer = list(best)
    answer = sorted(best)
    answer = ','.join(answer)
    print('Password: ', answer)

  def result1(self):
    trios = self.find_trios()
    total = 0
    for t in trios:
      if any(n[0] == 't' for n in t):
        print(t, ' => T')
        total +=1
      else:
        print(t)
    print('Total T', total)

  def result1(self):
    trios = self.find_trios()
    total = 0
    for t in trios:
      if any(n[0] == 't' for n in t):
        print(t, ' => T')
        total +=1
      else:
        print(t)
    print('Total T', total)

  def result(self):
    self.result2()


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

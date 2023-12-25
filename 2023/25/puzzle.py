import sys
import itertools

class Puzzle:

  def process(self, text):
    self.nodes = {}
    for line in text.split('\n'):
      self.process_line(line)

  def roots(self):
    possible = list(self.nodes.keys())
    linked = set()
    for n in self.nodes:
      for o in self.nodes[n]:
        linked.add(o)
    return list(set(possible)-linked)

  def process_line(self, line):
    if line != '':
      lhs, rhs = line.split(': ')
      rhs = rhs.split(' ')
      if lhs not in self.nodes:
        self.nodes[lhs] = []
      for r in rhs:
        if r not in self.nodes:
          self.nodes[r] = []
        self.nodes[lhs].append(r)

  def bfs_walk(self, r, cuts = []):
    tovisit = [r]
    visited = {}
    walked = []
    while tovisit:
      c = tovisit.pop(0)
      walked.append(c)
      for n in self.nodes[c]:
        if n not in visited and (c, n) not in cuts and (n, c) not in cuts:
          visited[n] = True
          tovisit.append(n)
    return set(walked) - {r}

  def result(self):
    roots = self.roots()
    nodecount = len(self.nodes)
    print(roots)
    print(len(roots), 'roots and', nodecount, 'nodes')
    print("="*80)
    #Walk each subtree in BFS order
    subtrees = {}
    for r in roots:
      subtrees[r] = self.bfs_walk(r)
      #print(r, subtrees[r])
    #For each PAIR of nodes, these could be the two new trees
    pairs = itertools.combinations(roots, 2)
    for a, b in pairs:
      ast = subtrees[a]
      bst = subtrees[b]
      notb = ast - bst
      nota = bst - ast
      #Determine the links for the ones NOT in one which link to the other
      potential = []
      for n in notb:
        other = self.nodes[n]
        for o in other:
          if o in bst:
            potential.append((n, o))
      for n in nota:
        other = self.nodes[n]
        for o in other:
          if o in ast:
            potential.append((n, o))
      if len(potential) >= 3:
        #print('Candidate:', a, b, '8<:', potential)
        sets = itertools.combinations(potential, 3)
        for cut in sets:
          ast = self.bfs_walk(a, cut)
          bst = self.bfs_walk(b, cut)
          #print(cut, ':', ast, bst, ast & bst)
          if ast & bst == set():
            #This is a pair of trees, but is it ALL the nodes?
            aval = len(ast) + 1 #self
            bval = len(bst) + 1 #self
            print(cut, '->', aval, bval, 'v', nodecount)
            if aval + bval == nodecount:
              print('Found')
              print(ast)
              print(bst)
              total = aval * bval
              print(aval, '*', bval, '=', total)
              return




if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

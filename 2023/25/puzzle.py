import sys
import itertools

class Puzzle:

  def process(self, text):
    self.nodes = {}
    self.topnodes = {}
    for line in text.split('\n'):
      self.process_line(line)

  def roots(self):
    possible = list(self.topnodes)
    linked = set()
    for n in possible:
      for o in self.topnodes[n]:
        linked.add(o)
    return list(set(possible)-linked)

  def process_line(self, line):
    if line != '':
      lhs, rhs = line.split(': ')
      rhs = rhs.split(' ')
      if lhs not in self.nodes:
        self.nodes[lhs] = set()
      if lhs not in self.topnodes:
        self.topnodes[lhs] = set()
      for r in rhs:
        if r not in self.nodes:
          self.nodes[r] = set()
        if r not in self.topnodes:
          self.topnodes[r] = set()

        self.topnodes[lhs].add(r)
        self.nodes[lhs].add(r)
        self.nodes[r].add(lhs)


  def bfs_walk(self, r, cuts = []):
    tovisit = [r]
    visited = {}
    walked = []
    while tovisit:
      c = tovisit.pop(0)
      walked.append(c)
      for n in self.topnodes[c]:
        if n not in visited:
          if (c, n) in cuts or (n, c) in cuts:
            continue
          visited[n] = True
          tovisit.append(n)

    return set(walked) - {r}

  def dbfs_walk(self, r, cuts = []):
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

  def path(self, start, end):
    tovisit = [(start, [])]
    visited = {}
    while tovisit:
      c, path = tovisit.pop(0)
      if c == end:
        return path
      for n in self.nodes[c]:
        if n not in visited:
          visited[n] = True
          tovisit.append((n, path + [c]))

    return set(walked) - {r}

  def result_x(self):
    nodecount = len(self.topnodes)
    links = []
    for k in self.topnodes:
      for n in self.topnodes[k]:
        links.append((k,n))
    #print(links)
    sets = itertools.combinations(links, 3)
    n = 0
    for cut in sets:
      n += 1
      if n % 1000 == 0:
        sys.stdout.write('.')
        sys.stdout.flush()
      t1 = cut[0][0]
      t2 = cut[0][1]
      ast = self.dbfs_walk(t1, cut)
      bst = self.dbfs_walk(t2, cut)
      aval = len(ast) + 1 #self
      bval = len(bst) + 1 #self
      #print(cut, t1, t2, aval, bval, ast-bst)
      if (aval + bval) == nodecount:
        print(cut, '->', aval, bval, 'v', nodecount)
        print(aval, '*', bval, '=', aval*bval)
        return


  def result(self):
    used = {}
    roots = self.roots()
    nodecount = len(self.nodes)
    print(roots)
    print(len(roots), 'roots and', nodecount, 'nodes')
    print("="*80)
    pairs = itertools.combinations(roots, 2)
    count = 0
    for a, b in pairs:
      path = self.path(a,b)
      #print(a, b, path)
      sys.stdout.write('.')
      sys.stdout.flush()
      for n in range(len(path)-1):
        s = path[n]
        e = path[n+1]
        #Init if never seen this combo
        if (s,e) not in used and (e,s) not in used:
          used[(s,e)] = 0

        if (s,e) in used:
          used[(s,e)] += 1
        else:
          used[(e,s)] += 1
    counts = []
    for l in used:
      counts.append((used[l], l))
    counts = sorted(counts, reverse=True)
    
    cuts = [counts[0][1], counts[1][1], counts[2][1]]
    print("Selected Cuts", cuts)
    a = cuts[0][0]
    b = cuts[0][1]
    ast = self.dbfs_walk(a, cuts)
    bst = self.dbfs_walk(b, cuts)
    aval = len(ast) + 1 #self
    bval = len(bst) + 1 #self
    print(cuts, '->', aval, bval, 'v', nodecount)
    print(aval, '*', bval, '=', aval*bval)

    #for i in range(0,10):
    #  print(counts[i])

    

  def result_x(self):
    seen = {}
    roots = self.roots()
    nodecount = len(self.nodes)
    #print(roots)
    print(len(roots), 'roots and', nodecount, 'nodes')
    print("="*80)

    #roots = list(self.nodes.keys())
    #Walk each subtree in BFS order
    subtrees = {}
    for r in roots:
      subtrees[r] = self.bfs_walk(r)
      #print(r, subtrees[r])
    #For each PAIR of nodes, these could be the two new trees
    pairs = itertools.combinations(roots, 2)
    count = 0
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
          if cut not in seen:
            seen[cut] = True
            count += 1
            if count % 100 == 0:
              sys.stdout.write('.')
              sys.stdout.flush()

            ast = self.dbfs_walk(a, cut)
            bst = self.dbfs_walk(b, cut)
            aval = len(ast) + 1 #self
            bval = len(bst) + 1 #self
            if aval + bval == nodecount:
              print('Found')
              print(ast)
              print(bst)
              total = aval * bval
              print(aval, '*', bval, '=', total)
              return
    print('Fail')




if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()


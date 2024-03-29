import sys

class Puzzle:

  def process(self, text):
    self.rows = []
    lines = text.split('\n')
    for line in lines:
      self.process_line(line)
    self.height = len(self.rows)
    self.width = len(self.rows[0])

  def process_line(self, line):
    if len(line) > 0:
      row = [int(ch) for ch in line]
      self.rows.append(row)

  def expand(self):
    #expand in X
    new_rows = []
    for row in self.rows:
      newrow = [r for r in  row]
      for i in range(1,5):
        for x in range(self.width):
          n = newrow[(self.width*(i-1))+x]
          n = (n % 9) + 1
          newrow.append(n)
      new_rows.append(newrow)
    self.rows = new_rows
    #expand in Y
    new_rows = [r for r in self.rows]
    for i in range(1,5):
      for y in range(self.height):
        row = [r for r in new_rows[(self.height*(i-1))+y]]
        print row
        newrow = []
        for n in row:
          m = (n % 9) + 1
          newrow.append(m)
        new_rows.append(newrow)
    self.rows = new_rows
    self.height = len(self.rows)
    self.width = len(self.rows[0])


  def to_str(self):
    dump = ""
    for row in self.rows:
      for n in row:
        dump += str(n)
      dump += '\n'
    return dump

  def naive_bests(self):
    bests = {(0,0): 0}
    parents = {}
    for y in range(self.height):
      if y > 0:
        cost = bests[(0, y-1)] + self.rows[y][0]
        parents[(0, y)]=(0,y-1)
      else:
        cost = 0
      row = self.rows[y]
      bests[(0, y)] = cost
      for x in range(1, self.width):
        bests[(x,y)] = bests[(x-1, y)] + self.rows[y][x]
        parents[(x, y)]=(x-1,y)
    return (bests, parents)

  def shortest_path(self):
    start = (0,0)
    end = (self.height-1, self.width-1)
    print 'Plotting', start, end
    tovisit = [(start, [], 0)]
    bests = {start:sys.maxint, end: sys.maxint}
    bests, parents = self.naive_bests()
    print 'Naive best', bests[end]
    #print bests
    #print parents
    changed = set([p for p in parents])
    while len(changed) > 0:
      print 'Processing', len(changed), 'changes'
      newchanged = set()
      for item in changed:
        neighbours = self.neighbours(item)
        #print item, neighbours
        pcost = bests[item]
        for neighbour in neighbours:
          x, y = neighbour
          cost = self.rows[y][x]
          if bests[neighbour] > pcost + cost:
            #This is better now
            bests[neighbour] = pcost + cost
            parents[neighbour] = item
            newchanged.add(neighbour)
      changed = newchanged
    cur = end
    path = []
    while cur != start:
      path = [cur] + path
      cur = parents[cur]
    path = [start] + path
    return (path, bests[end])

  def neighbours(self, loc):
    x, y = loc
    deltas = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    neighbours = []
    for d in deltas:
      dx, dy = d
      xx = x + dx
      yy = y + dy
      if xx >=0 and xx < self.width and yy >=0 and yy < self.height:
        neighbours.append((xx, yy))
    return neighbours

  def result(self):
    self.expand()
    print self.to_str()
    print self.shortest_path()

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

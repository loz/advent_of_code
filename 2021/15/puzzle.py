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

  def naive_bests(self):
    bests = {(0,0): 0}
    for y in range(self.height):
      if y > 0:
        cost = bests[(0, y-1)] + self.rows[y][0]
      else:
        cost = 0
      row = self.rows[y]
      bests[(0, y)] = cost
      for x in range(1, self.width):
        bests[(x,y)] = bests[(x-1, y)] + self.rows[y][x]
    return bests

  def shortest_path(self):
    start = (0,0)
    end = (self.height-1, self.width-1)
    print 'Plotting', start, end
    tovisit = [(start, [], 0)]
    bests = {start:sys.maxint, end: sys.maxint}
    bests = self.naive_bests()
    print 'Naive best', bests[end]
    #return
    #neighbours = self.neighbours(start)
    #for n in neighbours:
    #  tovisit.append((n, [start], bests[n]))
    bestpaths = {start:[]}
    while len(tovisit):
      cur = tovisit.pop()
      #print cur
      loc, path, cost = cur
      bloc = bests.get(loc, sys.maxint)
      if cost <= bloc and cost < bests[end]:
        bests[loc] = cost
        bestpaths[loc] = path + [loc]
        if loc == end:
          print 'Found path', cost, 'remaining', len(tovisit)
        neighbours = self.neighbours(loc)
        for neighbour in neighbours:
          nx, ny = neighbour
          ncost = cost + self.rows[ny][nx]
          nbest = bests.get(neighbour, sys.maxint)
          #only do if this is shortest path to here
          if ncost <= nbest: 
            #print 'Should visit', neighbour, ncost
            tovisit.append((neighbour, path + [loc], ncost))
    return (bestpaths[end], bests[end])

  def neighbours(self, loc):
    x, y = loc
    deltas = [(1, 0), (0, 1)]
    neighbours = []
    for d in deltas:
      dx, dy = d
      xx = x + dx
      yy = y + dy
      if xx >=0 and xx < self.width and yy >=0 and yy < self.height:
        neighbours.append((xx, yy))
    return neighbours

  def result(self):
    print self.shortest_path()

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input.1', 'r').read()
  puz.process(inp)
  puz.result()

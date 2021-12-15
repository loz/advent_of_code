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

  def shortest_path(self):
    start = (0,0)
    end = (self.height-1, self.width-1)
    print 'Plotting', start, end
    (path, cost) = self._visit(start, [], 0, end, {})
    print path, cost
    return path

  def _visit(self, loc, visited, cost, end, bests):
    visited = visited + [loc]
    if loc == end:
      return (visited, cost)
    #print loc, visited, cost, end
    neighbours = self.neighbours(loc)
    neighbours = filter(lambda n: n not in visited, neighbours)
    #print 'N',neighbours, loc
    best = sys.maxint
    bestpath = []
    for neighbour in neighbours:
      nx, ny = neighbour
      ncost = cost + self.rows[ny][nx]

      nbest = bests.get(neighbour, sys.maxint)
      if ncost < nbest: #only do if this is shortest path to here
        bests[neighbour] = ncost
        path, ncost = self._visit(neighbour, visited, ncost, end, bests)
        #print 'Visit via', path, ncost
        if ncost < best:
          best = ncost
          bestpath = path
    return (bestpath, best)

  def neighbours(self, loc):
    x, y = loc
    deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbours = []
    for d in deltas:
      dx, dy = d
      xx = x + dx
      yy = y + dy
      if xx >=0 and xx < self.width and yy >=0 and yy < self.height:
        neighbours.append((xx, yy))
    return neighbours

  def result(self):
    self.shortest_path()

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

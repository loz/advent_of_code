import itertools

class Puzzle:

  def process(self, text):
    self.markers = {}
    self.grid = []
    lines = text.split('\n')
    for line in lines:
      if line.strip() != '':
        self.process_line(line)
    self.width = len(self.grid[0])
    self.height = len(self.grid)

  def process_line(self, line):
    y = len(self.grid)
    row = [ch for ch in line]
    self.grid.append(row)
    for x in range(len(row)):
      ch = row[x]
      if ch != '#' and ch != '.':
        self.markers[int(ch)] = (x, y)

  def neighbours(self, loc):
    x, y = loc
    deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    locs = []
    for dxdy in deltas:
      dx, dy = dxdy
      xdx = x + dx
      ydy = y + dy
      if xdx > 0 and xdx <= self.width and ydy > 0 and ydy <= self.height:
        if self.grid[ydy][xdx] != '#':
          locs.append((xdx, ydy))
    return locs
  
  def bfs(self, start, finish):
    discovered = {start:True}
    head = [start]
    tail = []
    depth = 0
    while len(head) > 0:
      loc = head.pop(0)
      if loc == finish:
        return depth
      options = self.neighbours(loc)
      for option in options:
        if not discovered.has_key(option):
          discovered[option] = True
          tail.append(option)
      if len(head) == 0:
        depth += 1
        head = tail
        tail = []
    return 100000

  def result(self):
    markers = self.markers.keys()
    markers.sort()
    start = markers.pop(0)
    print 'Targets', markers
    options = itertools.permutations(markers)
    options = map(lambda o: list(o) + [start], options)
    shortest = None
    short_route = None
    for option in options:
      current = start
      path = list(option)
      length = 0
      while len(path) > 0:
        nextp = path.pop(0)
        length += self.bfs(self.markers[current], self.markers[nextp])
        if shortest != None and length > shortest:
          length = 100000
          break
        current = nextp
      #print start, '->', option, length
      if shortest == None or length < shortest:
        shortest = length
        short_route = option
        print shortest
    print 'Shortest Route', shortest, short_route

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

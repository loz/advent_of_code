import sys

class Puzzle:
  DELTAS = [
    (-1, 0), (1, 0), (0, -1), (0, 1)
  ]

  def process(self, text):
    self.heights = []
    for line in text.split('\n'):
      self.process_line(line)
    self.find_targets()

  def find_targets(self):
    for y in range(len(self.heights)):
      for x in range(len(self.heights[0])):
        if self.heights[y][x] == 'S':
          self.start = (x, y)
        elif self.heights[y][x] == 'E':
          self.end = (x,y)

  def moves_from(self, x, y):
    options = []
    current = self.map(x, y)
    if current == 'E':
      current = 'z'
    if current == 'S':
      current = 'a'
    for d in self.DELTAS:
      dx, dy = d
      tx = x+dx
      ty = y+dy
      if tx < 0 or tx == len(self.heights[0]):
        continue
      if ty < 0 or ty == len(self.heights):
        continue

      th = self.map(tx, ty)
      if ord(current) >= ord(th):
        options.append((tx, ty))
      elif ord(current) == ord(th)-1:
        options.append((tx, ty))
    return options

  def map(self, x,y):
    return self.heights[y][x]

  def process_line(self, line):
    if line != '':
      row = [ch for ch in line]
      self.heights.append(row)

  def bfs(self, loc, visited, distance):
    if loc == self.end:
      print 'Found, at', distance
      return
    options = self.moves_from(loc[0], loc[1])
    for o in options:
      if o not in visited:
        self.bfs(o, visited + [loc], distance +1)

  def dijk(self):
    distances = {self.start: 0}
    visited = {}
    tovisit = [self.start]
    paths = {self.start:[self.start]}

    while len(tovisit) > 0:
      loc = tovisit.pop()
      dist = distances.get(loc)
      curpath = paths[loc]
      visited[loc] = True
      options = self.moves_from(loc[0], loc[1])
      for o in options:
        if visited.get(o, False):
          if distances[o] > dist + 1:
            distances[o] = dist + 1
            paths[o] = curpath + [o]
            tovisit.append(o)
        else:
          distances[o] = dist + 1
          paths[o] = curpath + [o]
          tovisit.append(o)
    print 'Distance to E', distances[self.end]
    path = paths[self.end]
    for y in range(len(self.heights)):
      for x in range(len(self.heights[0])):
        if (x,y) in path:
          sys.stdout.write(u"\u001b[36m" + self.heights[y][x])
        else:
          sys.stdout.write(u"\u001b[0m" + self.heights[y][x])
      print
  
    
  def result(self):
    self.dijk()



if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

class Puzzle:

  def process(self, text):
    self.map = []
    lines = text.split('\n')
    for line in lines:
      self.process_line(line)
    self.height = len(self.map)
    self.width = len(self.map[0])

  def process_line(self, line):
    if len(line) != 0:
      row = [int(ch) for ch in line]
      self.map.append(row)
      

  def identify_lows(self):
    #print self.map, self.size
    lows = []
    for y in range(self.height):
      for x in range(self.width):
        height = self.map[y][x]
        neighbours = self.neighbours(x,y)
        larger = filter(lambda x: height >= x[1], neighbours)
        #print height, neighbours, larger
        if len(larger) == 0:
          lows.append(((x,y), height))
    return lows

  def size_basin(self, low):
    visited = []
    tovisit = [low]
    while len(tovisit) > 0:
      loc = tovisit.pop()
      visited.append(loc)
      xy, h = loc
      x, y = xy
      neighbours = self.neighbours(x,y)
      for n in neighbours:
        if n[1] >= h and n[1] != 9:
          if n not in visited and n not in tovisit:
            tovisit.append(n)
    print visited
    return len(visited)

  def neighbours(self, x, y):
    deltas = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    values = []
    for d in deltas:
      dx, dy = d
      nx = x + dx
      ny = y + dy
      if ny >= 0 and ny < self.height and nx >= 0 and nx < self.width:
         values.append(((nx,ny),self.map[ny][nx]))
    return values

  def result(self):
    lows = self.identify_lows()
    risk = 0
    basins = []
    for low in lows:
      xy, h = low
      risk += 1 + h
      basin_size = self.size_basin(low)
      print low, basin_size
      basins.append(basin_size)
    print 'Risk', risk
    print 'Basin', basins
    basins.sort(reverse=True)
    print 'Max:', basins[0] * basins[1] * basins[2]


if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

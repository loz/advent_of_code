class Puzzle:

  def process(self, text):
    self.grid = []
    lines = text.split('\n')
    for line in lines:
      self.process_line(line)
    self.height = len(self.grid)
    self.width = len(self.grid[0])

  def process_line(self, line):
    if len(line) > 0:
      row = [int(ch) for ch in line]
      self.grid.append(row)

  def step(self):
    self.increase_engergy()
    count = self.flash()
    self.reset_flashed()
    return count

  def reset_flashed(self):
    for y in range(self.height):
      for x in range(self.width):
        if self.grid[y][x] > 9:
          self.grid[y][x] = 0

  def flash(self):
    to_flash = []
    flashed = []
    for y in range(self.height):
      for x in range(self.width):
        if self.grid[y][x] > 9:
          to_flash.append((x,y))
    while len(to_flash) > 0:
      octo = to_flash.pop()
      flashed.append(octo)
      impact = self.neighbours(octo[0], octo[1])
      #print 'Flash', octo, impact
      for n in impact:
        nx, ny = n
        self.grid[ny][nx] += 1
        if self.grid[ny][nx] > 9 and n not in to_flash and n not in flashed:
          to_flash.append(n)
    return len(flashed)
        
  
  def neighbours(self, x, y):
    deltas = [(-1,-1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    neighbours = []
    for d in deltas:
      dx, dy = d
      xx = x + dx
      yy = y + dy
      if xx >= 0 and xx < self.width and yy >= 0 and yy < self.height:
        neighbours.append((xx, yy))
    return neighbours

  def increase_engergy(self):
    for y in range(self.height):
      for x in range(self.width):
        self.grid[y][x] += 1

  def to_str(self):
    mapstring = ""
    for row in self.grid:
      for i in row:
        mapstring +=  str(i)
      mapstring += '\n'
    return mapstring

  def result1(self):
    flashes = 0
    print self.to_str()
    for i in range(100):
      flashes += self.step()
      print 'Step', i+1
      print self.to_str()
    print 'Total Flashes', flashes

  def result(self):
    flashes = 0
    print self.to_str()
    #for i in range(200):
    i = 0
    while True:
      count = self.step()
      flashes += count
      print 'Step', i+1
      if count == 100:
        print self.to_str()
        print '100 Flashes!'
        return
      #print self.to_str()
      i += 1
    print 'Total Flashes', flashes

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

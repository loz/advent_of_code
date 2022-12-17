import sys

BLOCKS = [
  ("####", (4,1)),  #block, widthxheight
  (" # \n###\n # ", (3,3)),
  ("  #\n  #\n###", (3,3)),
  ("#\n#\n#\n#", (1, 4)),
  ("##\n##", (2,2))
]



class Puzzle:
  def __init__(self):
    self.falling = 0
    self.pos = (2, 3)
    self.rockface = []
    self.height = 0

  def process(self, text):
    self.wind = []

    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      for ch in line:
        if ch == '>':
          self.wind.append(1)
        else:
          self.wind.append(-1)
 
  def dump(self):
    print ""
    for y in range(self.height):
      row = self.rockface[self.height-1-y]
      sys.stdout.write('|')
      for r in row:
        if r:
          sys.stdout.write('#')
        else:
          sys.stdout.write('.')
      print '|'
    print "+-------+"

  def rock_at(self, x, y):
    if y >= self.height or y < 0:
      return False
    return self.rockface[y][x]

  def land_rock(self, rx, ry):
    #print "land at", rx, ry
    shape, size = BLOCKS[self.falling]
    #Expand rockface
    while ry+size[1] > self.height:
      self.rockface.append([False, False, False, False, False, False, False])
      self.height += 1
    rows = shape.split('\n')
    oy = ry+size[1]-1
    for y in range(size[1]):
      for x in range(size[0]):
        if rows[y][x] == '#':
          self.rockface[oy-y][rx+x] = True
    self.falling = (self.falling + 1) % 5
    nx = 2
    ny = self.height+3
    self.pos = (nx, ny)

  def can_fall(self, shape, size, rx, ry):
    if ry <= 0: #TODO
      return False
    rows = shape.split('\n')
    oy = ry+size[1]-1
    for y in range(size[1]):
        for x in range(size[0]):
          #print 'Check', (x, y), (rx+x, oy-y-1)
          if rows[y][x] == '#':
            if self.rock_at(rx+x, oy-y-1):
              #print 'Hit Rock'
              return False
    return True
  
  def can_blow(self, shape, size, rx, ry, wind):
    if (rx + wind + size[0]) > 7 or rx + wind < 0:
      return False
    rows = shape.split('\n')
    oy = ry+size[1]-1
    for y in range(size[1]):
        for x in range(size[0]):
          #print 'Check', (x, y), (rx+x, oy-y-1)
          if rows[y][x] == '#':
            if self.rock_at(rx+x+wind, oy-y):
              #print 'Hit Rock'
              return False
    return True
    

  def tick(self):
    didland = False
    shape, size = BLOCKS[self.falling]
    wind = self.wind.pop(0)
    x, y = self.pos
    nx = x + wind
    if self.can_blow(shape, size, x, y, wind):
      nx = x + wind
    else:
      nx = x
    if self.can_fall(shape, size, nx, y):
      ny = y - 1
      self.pos = (nx, ny)
    else:
      self.land_rock(nx, y)
      didland = True
    self.wind.append(wind)
    return didland

  def result(self):
    for t in range(2022):
      while not self.tick():
        pass
    self.dump()
    print 'Height', self.height




if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

class Puzzle:

  def process(self, text):
    lines = text.split('\n')
    lines = filter(lambda l: l.strip() != '', lines)
    self.minx = 0
    self.miny = 0
    self.minz = 0
    self.maxx = len(lines[0])-1
    self.maxy = len(lines)-1
    self.maxz = 0
    plane = {}
    for y in range(self.miny, self.maxy+1):
      row = {}
      for x in range(self.minx, self.maxx+1):
        row[x] = lines[y][x]
      plane[y] = row
    self.cube = {0: plane}


  def fetch_cell(self, x, y, z):
    z = abs(z) #reflects along z axis always
    try:
      return self.cube[z][y][x]
    except:
      return '.'
  
  def neighbours(self, x, y, z):
    neighbours = []
    for dz in range(-1, 2):
      for dy in range(-1, 2):
        for dx in range(-1, 2):
          if dy == dz == dx == 0:
            pass
          else:
            neighbours.append(self.fetch_cell(x+dx, y+dy, z+dz))
    return neighbours
 
  def set_cell(self, cube, x, y, z):
    if cube.has_key(z):
      if cube[z].has_key(y):
        cube[z][y][x] = '#'
      else:
        cube[z][y] = {x:'#'}
    else:
      cube[z] = {y:{x:'#'}}
    return cube
      

  def tick(self):
    newcube = {}
    minx = self.minx
    miny = self.miny
    maxx = self.maxx
    maxy = self.maxy
    maxz = self.maxz
    for z in range(-1, self.maxz+2): #z reflects so -1 is sufficient, as it is == 1
      for y in range(self.miny-1, self.maxy+2):
        for x in range(self.minx-1, self.maxx+2):
          cell = self.fetch_cell(x, y, z)
          neighbours = self.neighbours(x, y, z)
          full = neighbours.count('#')
          if cell == '#': #active
            if full == 2 or full == 3:
              newcube = self.set_cell(newcube, x, y, z)
              if x < minx:
                minx = x
              if y < miny:
                miny = y
              if x > maxx:
                maxx = x
              if y > maxy:
                maxy = y
              if z > maxz:
                maxz = z
          else:
            if full == 3:
              newcube = self.set_cell(newcube, x, y, z)
              if x < minx:
                minx = x
              if y < miny:
                miny = y
              if x > maxx:
                maxx = x
              if y > maxy:
                maxy = y
              if z > maxz:
                maxz = z
    self.minx = minx
    self.miny = miny
    self.maxx = maxx
    self.maxy = maxy
    self.maxz = maxz
    self.cube = newcube

  def slice(self, z):
    z = abs(z)
    string = ""
    for y in range(self.miny, self.maxy+1):
      for x in range(self.minx, self.maxx+1):
        string += self.fetch_cell(x, y, z)
      string += '\n'
    return string

  def result(self):
    for t in range(6):
      self.tick()

    for z in range(0, self.maxz+1):
      print z
      print self.slice(z)
    total = 0
    zero = self.cube[0]
    ztotal = 0
    for y in zero:
      ztotal += len(zero[y])
    #print ztotal
    for z in range(1, self.maxz+1):
      for y in self.cube[z]:
        total += len(self.cube[z][y])
    #print ztotal, total
    count = (total * 2) + ztotal
    print count

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

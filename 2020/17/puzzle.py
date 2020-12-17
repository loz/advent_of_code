class Puzzle:

  def process(self, text):
    lines = text.split('\n')
    lines = filter(lambda l: l.strip() != '', lines)
    self.minx = 0
    self.miny = 0
    self.minz = 0
    self.minw = 0
    self.maxx = len(lines[0])-1
    self.maxy = len(lines)-1
    self.maxz = 0
    self.maxw = 0
    plane = {}
    for y in range(self.miny, self.maxy+1):
      row = {}
      for x in range(self.minx, self.maxx+1):
        row[x] = lines[y][x]
      plane[y] = row
    self.cube = {0: {0: plane}}


  def fetch_cell(self, x, y, z, w):
    z = abs(z) #reflects along z axis always
    w = abs(w) #reflects along w axis always
    try:
      return self.cube[w][z][y][x]
    except:
      return '.'
  
  def neighbours(self, x, y, z, w):
    neighbours = []
    for dw in range(-1, 2):
      for dz in range(-1, 2):
        for dy in range(-1, 2):
          for dx in range(-1, 2):
            if dy == dz == dx == dw == 0:
              pass
            else:
              neighbours.append(self.fetch_cell(x+dx, y+dy, z+dz, w+dw))
    return neighbours
 
  def set_cell(self, cube, x, y, z, w):
    if cube.has_key(w):
      if cube[w].has_key(z):
        if cube[w][z].has_key(y):
          cube[w][z][y][x] = '#'
        else:
          cube[w][z][y] = {x:'#'}
      else:
        cube[w][z] = {y:{x:'#'}}
    else:
      cube[w] = {z: {y:{ x:'#'}}}
    return cube
      

  def tick(self):
    newcube = {}
    minx = self.minx
    miny = self.miny
    maxx = self.maxx
    maxy = self.maxy
    maxz = self.maxz
    maxw = self.maxw
    for w in range(0, self.maxw+2): #w reflects on 0 is sufficient, as -1 == 1
      for z in range(0, self.maxz+2): #z reflects on 0 is sufficient, as -1 == 1
        for y in range(self.miny-1, self.maxy+2):
          for x in range(self.minx-1, self.maxx+2):
            cell = self.fetch_cell(x, y, z, w)
            neighbours = self.neighbours(x, y, z, w)
            full = neighbours.count('#')
            if cell == '#': #active
              if full == 2 or full == 3:
                newcube = self.set_cell(newcube, x, y, z, w)
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
                if w > maxw:
                  maxw = w
            else:
              if full == 3:
                newcube = self.set_cell(newcube, x, y, z, w)
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
                if w > maxw:
                  maxw = w
    self.minx = minx
    self.miny = miny
    self.maxx = maxx
    self.maxy = maxy
    self.maxz = maxz
    self.maxw = maxw
    self.cube = newcube

  def slice(self, z):
    z = abs(z)
    string = ""
    for y in range(self.miny, self.maxy+1):
      for x in range(self.minx, self.maxx+1):
        string += self.fetch_cell(x, y, z)
      string += '\n'
    return string

  def slice2(self, z, w):
    z = abs(z)
    w = abs(w)
    string = ""
    for y in range(self.miny, self.maxy+1):
      for x in range(self.minx, self.maxx+1):
        string += self.fetch_cell(x, y, z, w)
      string += '\n'
    return string

  def result(self):
    #for z in range(0, self.maxz+1):
    for w in range(0, self.maxw+1):
      for z in range(0, self.maxz+1):
        print 'z=', z, 'w=', w
        print self.slice2(z,w)

    for t in range(6):
      print t+1
      self.tick()

    #for z in range(0, self.maxz+1):
    for w in range(0, self.maxw+1):
      for z in range(0, self.maxz+1):
        print 'z=', z, 'w=', w
        print self.slice2(z,w)
    
    total = 0
    for w in range(-1*self.maxw, self.maxw+1):
      for z in range(-1*self.maxz, self.maxz+1):
        for y in range(self.miny, self.maxy+1):
          for x in range(self.minx, self.maxx+1):
            if self.fetch_cell(x, y, z, w) == '#':
              total = total + 1
    print total

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

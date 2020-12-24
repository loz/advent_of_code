EVEN_DELTAS = {
  'e' : ( 1, 0),
  'w' : (-1, 0),
  'nw': ( 0,-1),
  'ne': ( 1,-1),
  'sw': ( 0, 1),
  'se': ( 1, 1),
}

ODD_DELTAS = {
  'e' : ( 1, 0),
  'w' : (-1, 0),
  'nw': (-1,-1),
  'ne': ( 0,-1),
  'sw': (-1, 1),
  'se': ( 0, 1),
}

IMG = {
  'black': '.',
  'white': '#',
}

class Puzzle:


  def process(self, text):
    self.directions = []
    self.tiles = {}
    lines = text.split('\n')
    for line in lines:
      if line.strip() != '':
        self.directions.append(self.parse_directions(line))
    self.follow_directions()

  def follow_directions(self):
    for path in self.directions:
      x = 0
      y = 0
      for bearing in path:
        #print x, y, bearing
        if abs(y) % 2 == 0:
          dx, dy = EVEN_DELTAS[bearing]
          #print 'even', dx, dy
        else:
          dx, dy = ODD_DELTAS[bearing]
          #print 'odd', dx, dy
        x += dx
        y += dy
      #print (x,y)
      if self.tile_at(x, y) == 'white':
        self.set_tile(x, y, 'black')
      else:
        self.set_tile(x, y, 'white')

  def set_tile(self, x, y, colour):
    loc = (x, y)
    self.tiles[loc] = colour

  def tile_at(self, x, y):
    loc = (x, y)
    if self.tiles.has_key(loc):
      return self.tiles[loc]
    else:
      return 'white'
  
  def parse_directions(self, line):
    chars = [ch for ch in line]
    dirs = []
    while len(chars) > 0:
      ch = chars.pop(0)
      if ch == 'e' or ch == 'w':
        dirs.append(ch)
      else:
        be = chars.pop(0)
        dirs.append(ch + be)
    return dirs

  def tick(self):
    locs = self.tiles.keys()
    minx = min(locs, key=lambda l: l[0])[0]
    miny = min(locs, key=lambda l: l[1])[1]
    maxx = max(locs, key=lambda l: l[0])[0]
    maxy = max(locs, key=lambda l: l[1])[1]
    newtiles = {}
    even_deltas = map(lambda k: EVEN_DELTAS[k], EVEN_DELTAS)
    odd_deltas  = map(lambda k: ODD_DELTAS[k], ODD_DELTAS)
    for y in range(miny-1, maxy+2):
      for x in range(minx-1, maxx+2):
        if abs(y) % 2 == 0:
          deltas = even_deltas
        else:
          deltas = odd_deltas
        neighbours = map(lambda dxdy: self.tile_at(x+dxdy[0], y+dxdy[1]),deltas)
        numblack = neighbours.count('black')
        if self.tile_at(x,y) == 'black':
          if numblack == 0 or numblack > 2:
            newtiles[(x,y)] = 'white'
          else:
            newtiles[(x,y)] = 'black'
        else:
          if numblack == 2:
            newtiles[(x,y)] = 'black'
          else:
            newtiles[(x,y)] = 'white'
    self.tiles = newtiles


  def dump_tiles(self):
    locs = self.tiles.keys()
    minx = min(locs, key=lambda l: l[0])[0]
    miny = min(locs, key=lambda l: l[1])[1]
    maxx = max(locs, key=lambda l: l[0])[0]
    maxy = max(locs, key=lambda l: l[1])[1]
    #print minx, miny, '->', maxx, maxy
    for y in range(miny, maxy+1):
      if abs(y) % 2 == 0:
        print '',
      for x in range(minx, maxx+1):
        print IMG[self.tile_at(x, y)],
      print ''

  def count_black(self):
    total = 0
    for loc in self.tiles:
      tile = self.tiles[loc]
      if tile == 'black':
        total += 1
    return total
    

  def result1(self):
    total = 0
    for loc in self.tiles:
      tile = self.tiles[loc]
      #print loc, tile
      if tile == 'black':
        total += 1
    print 'Total Black:', total
    self.dump_tiles()

  def result(self):
    print 'Start Black:', self.count_black()
    self.dump_tiles()
    print '=========='
    day = 1
    for i in range(100):
      self.tick()
      #self.dump_tiles()
      print 'Day', day, ':', self.count_black()
      day += 1

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

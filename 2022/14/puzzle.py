import sys

class Puzzle:

  def map_at(self, x, y):
    return self.map.get((x,y), None)

  def process(self, text):
    self.map = {}
    for line in text.split('\n'):
      self.process_line(line)
    self.get_bounds()

  def get_bounds(self):
    minx = 99999
    maxx = -99999
    depth = 0
    for loc in self.map.keys():
      x, y = loc
      if minx > x:
        minx = x
      if maxx < x:
        maxx = x
      if depth < y:
        depth = y
    self.leftx = minx
    self.rightx = maxx
    self.depth = depth

  def process_line(self, line):
    if line != '':
      parts = line.split(' -> ')
      parts = self.map_parts(parts)
      self.plot_lines(parts)

  def map_parts(self, parts):
    coords = []
    for coord in parts:
      left, right = coord.split(',')
      left = int(left)
      right = int(right)
      coords.append((left, right))
    return coords

  def plot_lines(self, points):
    mpoints = [point for point in points]
    cx, cy = mpoints.pop(0)
    while mpoints:
      nx, ny = mpoints.pop(0)
      if cx == nx: #plot vertical
        start = min(cy, ny)
        finish = max(cy, ny)
        for y in range(start, finish+1):
          self.map[(cx, y)] = '#'
      else: #plot horiz
        start = min(cx, nx)
        finish = max(cx, nx)
        for x in range(start, finish+1):
          self.map[(x, cy)] = '#'
      cx, cy = nx, ny

  def dump(self):
    for y in range(self.depth+1):
      for x in range(self.leftx, self.rightx+1):
        ch = self.map_at(x, y)
        if ch:
          sys.stdout.write(ch)
        else:
          sys.stdout.write('.')
      print

  def drop_sand(self):
    sx = 500
    sy = 0
    falling = True
    while falling:
      if self.map_at(sx, sy+1) == None:
        sy += 1
      else:
        if self.map_at(sx-1, sy+1) == None: #Fall left
          sx -= 1
          #sy += 1
        elif self.map_at(sx+1, sy+1) == None: #Fall right
          sx += 1
          #sy += 1
        else:
          falling = False
      if sy == self.depth:
        return False
    self.map[(sx, sy)] = 'o'
    return True

  def result(self):
    fallen = 0
    while self.drop_sand():
      fallen += 1
      print u"\033[0;0H"
      self.dump()
    print fallen, 'sand landed'



if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

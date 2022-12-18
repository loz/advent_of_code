import sys

DELTAS = [
  (-1, 0, 0),
  (0, -1, 0),
  (0, 0, -1),
  (1, 0, 0),
  (0, 1, 0),
  (0, 0, 1)
]

class Puzzle:

  def process(self, text):
    self.cubes = {}
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      points = line.split(',')
      cube = (int(points[0]), int(points[1]), int(points[2]))
      self.cubes[cube] = True

  def surface(self, cube):
    count = 0
    for d in DELTAS:
      x, y, z = cube
      dx, dy, dz = d
      nx = x + dx
      ny = y + dy
      nz = z + dz
      if not self.cubes.get((nx, ny, nz), False):
        count += 1
    return count

  def water_surface(self, cube, water):
    count = 0
    for d in DELTAS:
      x, y, z = cube
      dx, dy, dz = d
      nx = x + dx
      ny = y + dy
      nz = z + dz
      if (nx, ny, nz) in water:
        count += 1
    return count

  def result1(self):
    total = 0
    for cube in self.cubes.keys():
      total += self.surface(cube)
    print 'Total Surface', total

  def getbounds(self):
    minx, miny, minz = 999999, 999999, 999999
    maxx, maxy, maxz = 0, 0, 0
    for cube in self.cubes.keys():
      x, y, z = cube
      minx = min([minx, x])
      miny = min([miny, y])
      minz = min([minz, z])
      maxx = max([maxx, x])
      maxy = max([maxy, y])
      maxz = max([maxz, z])
    return ((minx, miny, minz), (maxx, maxy, maxz))

  def neighbors(self, loc, bounds):
    _, maxb = bounds
    x, y, z = loc
    locs = []
    for d in DELTAS:
      dx, dy, dz = d
      nx = x + dx
      if nx < -1 or nx > maxb[0]+1:
        continue
      ny = y + dy
      if ny < -1 or ny > maxb[1]+1:
        continue
      nz = z + dz
      if nz < -1 or nz > maxb[2]+1:
        continue
      locs.append((nx, ny, nz))
    return locs

  def result(self):
    bounds = self.getbounds()
    print bounds
    #traverse water
    water = (0,0,0)
    visited = []
    edges = set()
    tovisit = [water]
    while tovisit:
      water = tovisit.pop()
      visited.append(water)
      neighbors = self.neighbors(water, bounds)
      for n in neighbors:
        if n not in visited:
          if self.cubes.get(n, False):
            edges.add(n) #found an edge
          else:
            tovisit.append(n)
    print 'Found', len(list(edges)), 'edge cubes'
    surface = 0
    for cube in edges:
      surface += self.water_surface(cube, visited)
    print 'Surface area', surface

if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

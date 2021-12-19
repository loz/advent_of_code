import itertools as it

def rx90(x, y, z):
  return (x, 0-z, y)

def ry90(x, y, z):
  return (z, y, 0-x)

def rz90(x, y, z):
  return (y, 0-x, z)

class Puzzle:
  def __init__(self):
    self.scanners = []
    self.world = set([])

  def process(self, text):
    lines = text.split('\n')
    self.current = -1
    for line in lines:
      if len(line) > 0:
        self.process_line(line)
    self.ref = self.scanners[0]
    self.add_to_world(self.ref)

  def find_overlaps(self, set1, set2):
    overlaps = []
    return overlaps

  def add_to_world(self, points):
    for p in points:
      self.world.add(p)

  def process_line(self, line):
    if line.startswith('---'):
      #line = line.replace('--- scanner ', '')
      #line = line.replace(' ---', '')
      #num = int(line)
      #print 'New Set', num
      self.current += 1
      self.scanners.append(set([]))
    else:
      parts = line.split(',')
      points = map(lambda c: int(c), parts)
      self.scanners[self.current].add((points[0], points[1], points[2]))

  def offset(self, coords, frompoint):
    newcords = []
    for c in coords:
      nc = [c[0]-frompoint[0], c[1]-frompoint[1], c[2]-frompoint[2]]
      newcords.append(nc)
    return newcords

  def rotations(self, point):
    x, y, z = point
    return [
      ( x, y, z),
      ( x, z,-y),
      ( x,-y,-z),
      ( x,-z, y),

      (-x, z, y),
      (-x, y,-z),
      (-x,-y, z),
      (-x,-z,-y),

      ( y, x,-z),
      ( y,-x, z),
      ( y, z, x),
      ( y,-z,-x),

      (-y, x, z),
      (-y,-x,-z),
      (-y,-z, x),
      (-y, z,-x),

      ( z, x, y),
      ( z,-x,-y),
      ( z,-y, x),
      ( z, y,-x),

      (-z, x,-y),
      (-z,-x, y),
      (-z, y, x),
      (-z,-y,-x)

    ]

  def rotations_slow(self, point):
    rotations = set([])
    x, y, z = point
    #This is daft in that there's overlap but set takes care
    for rx in range(4):
      x, y, z = rx90(x, y, z)
      for ry in range(4):
        x, y, z = ry90(x, y, z)
        for rz in range(4):
          x, y, z = rz90(x, y, z)
          rotations.add((x, y, z))
    return rotations

  def result(self):
    pass

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

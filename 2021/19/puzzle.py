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

  def gen_orientations(self, aset):
    orientations = []
    for i in range(24):
      orientations.append(set([]))

    for p in aset:
      rotations = self.rotations(p)
      counter = 0
      for r in rotations:
        orientations[counter].add(r)
        counter += 1
    return orientations

  def find_overlaps(self, set1, set2, beacons):
    #For each orientation of set2:
    orientations = self.gen_orientations(set2)
    obeacons = self.gen_orientations(beacons)
    #print obeacons
    for o in range(len(orientations)):
      o_set = orientations[o]
      o_bea = obeacons[o]
      #For each point in set1
      for p1 in set1:
          #For each point in o_set2
        for p2 in o_set:
          offset = (p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2])
          offsets = self.offset(o_set, offset)
          overlap = set1 & offsets
          if len(overlap) >= 12:
            #print 'Overlap!'
            #print (p1, p2), offset
            offset_bea = self.offset(o_bea, offset)
            return overlap, offsets, offset_bea
            #offset between set1, o_set2 -> newset
            #overlaps = set1 and newset?
    return set([]), [], beacons

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
    newcords = set([])
    for c in coords:
      nc = (c[0]-frompoint[0], c[1]-frompoint[1], c[2]-frompoint[2])
      newcords.add(nc)
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
  
  def reduce(self, topair):
    paird = []
    while len(topair) > 1:
      first = topair[0][0]
      firstbeacons = topair[0][1]
      topair = topair[1:]
      #print 'Pairing', first
      didpair = False
      for other in topair:
        otherset, otherbeacons = other
        overlaps, mapped, mappedbeacons = self.find_overlaps(first, otherset, otherbeacons)
        if len(overlaps) > 0:
          #merge
          newset = first | mapped
          newbeacons = firstbeacons | mappedbeacons
          paird.append((newset, newbeacons))
          topair.remove(other)
          didpair = True
          break
      if not didpair:
        print 'Did not pair'
        paird.append((first, firstbeacons))
    return paird + topair

  def result(self):
    # (set, [arr of beacon locations])
    topair = [(s, set([(0,0,0)])) for s in self.scanners]
    while len(topair) > 1:
      print 'Now Have', len(topair), 'sets'
      topair = self.reduce(topair)
    points, beacons = topair[0]
    print len(points), 'beacons'
    pairs = it.combinations(beacons, 2)
    largest = 0
    for pair in pairs:
      p1, p2 = pair
      distance = abs(p1[0]-p2[0]) + abs(p1[1]-p2[1]) + abs(p1[2]-p2[2])
      print distance
      if distance > largest:
        largest = distance

    print 'Furthest distance', largest

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

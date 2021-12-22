def overlap(cube1, cube2):
  corners1 = corners(cube1)
  corners2 = corners(cube2)
  in1 = pointsin(cube1, corners2)
  in2 = pointsin(cube2, corners1)
  return len(in1) + len(in2) > 0

def length(a, b):
  mmin = min(a,b)
  mmax = max(a,b)
  return abs(mmin - (mmax+1))

def is_in(bigger, smaller):
  small_corners = corners(smaller)
  in_bigger = pointsin(bigger, small_corners)
  return len(in_bigger) == 8

def corners(cube):
  x, y, z = cube
  return [
    (x[0], y[0], z[0]),
    (x[0], y[1], z[0]),
    (x[0], y[1], z[1]),
    (x[0], y[0], z[1]),

    (x[1], y[0], z[0]),
    (x[1], y[1], z[0]),
    (x[1], y[1], z[1]),
    (x[1], y[0], z[1]),
  ]

def pointsin(cube, points):
  x, y, z = cube
  inlist = []
  for p in points:
    px, py, pz = p
    if px >= x[0] and px <= x[1] and \
       py >= y[0] and py <= y[1] and \
       pz >= z[0] and pz <= z[1]:
      inlist.append(p)
  return inlist

def planer_cut_x(cube, x):
  cx, cy, cz = cube
  return [
    ((cx[0], x-1), cy, cz),
    ((x,   cx[1]), cy, cz)
  ]

def planer_cut_y(cube, y):
  cx, cy, cz = cube
  return [
    (cx, (cy[0], y-1), cz),
    (cx, (y,   cy[1]), cz)
  ]

def planer_cut_z(cube, z):
  cx, cy, cz = cube
  return [
    (cx, cy, (cz[0], z-1)),
    (cx, cy, (z,   cz[1]))
  ]

def subdivide(cube, point):
  x, y, z = point
  cubes = []
  left, right = planer_cut_x(cube, x)
  cubes.append(left)
  left, right = planer_cut_y(right,y)
  cubes.append(left)
  left, right = planer_cut_z(right,z)
  cubes.append(left)
  cubes.append(right)
  return cubes

def subdivide_with_2(cube, p1, p2):
  cubes = []
  if p1[0] == p2[0]: #Share X
    left, right = planer_cut_x(cube, p1[0])
    cubes.append(left)
    if p1[1] == p2[1]: #Share XY
      left, right = planer_cut_y(right, p1[1])
      cubes.append(left)
      #Threeway cut Z
      left, right = planer_cut_z(right, p1[2])
      cubes.append(left)
      left, right = planer_cut_z(right, p2[2])
      cubes.append(left)
      cubes.append(right)
    else:  #Share XZ
      left, right = planer_cut_z(right, p1[2])
      cubes.append(left)
      #Threeway cut Y
      left, right = planer_cut_y(right, p1[1])
      cubes.append(left)
      left, right = planer_cut_y(right, p2[1])
      cubes.append(left)
      cubes.append(right)
  elif p1[1] == p2[1]: #Share YZ
    left, right = planer_cut_y(cube, p1[1])
    cubes.append(left)
    left, right = planer_cut_z(right, p1[2])
    cubes.append(left)
    #Threeway cut X
    left, right = planer_cut_x(right, p1[0])
    cubes.append(left)
    left, right = planer_cut_x(right, p2[0])
    cubes.append(left)
    cubes.append(right)
  else:
    print 'Error, Z Not share X, or Y!'
    raise 'Oopsie'
  return cubes
  
def subdivide_old(cube, point):
  x, y, z = point
  cx, cy, cz = cube
  return [
    #(From Top Corners)
    #x1,y1,z1 -> px-1, py-1, pz-1
    ((cx[0],x-1), (cy[0],y-1), (cz[0],z-1)),
    #x2,y1,z1 -> px  , py-1, pz-1
    ((cx[1],x  ), (cy[0],y-1), (cz[0],z-1)),
    #x1,y1,z2 -> px-1, py-1, pz
    ((cx[0],x-1), (cy[0],y-1), (cz[1],z  )),
    #x2,y1,z2 -> pz  , py-1, pz
    ((cx[1],x  ), (cy[0],y-1), (cz[1],z  )),
    #(From Bottom Corners)
    #x1,y2,z1 -> px-1, py  , pz-1
    ((cx[0],x-1), (cy[1],y  ), (cz[0],z-1)),
    #x2,y2,z1 -> px  , py  , pz-1
    ((cx[1],x  ), (cy[1],y  ), (cz[0],z-1)),
    #x1,y2,z2 -> px-1, py  , pz
    ((cx[0],x-1), (cy[1],y  ), (cz[1],z  )),
    #x2,y2,z2 -> pz  , py  , pz
    ((cx[1],x  ), (cy[1],y  ), (cz[1],z  )),
  ]

def combine(cube1, cube2):
  newcubes = []
  print cube1, cube2
  x1, y1, z1 = cube1
  x2, y2, z2 = cube2
  corners2 = corners(cube2)
  points_in_1 = pointsin(cube1, corners2)
  print cube2, 'corners In', cube1, 'are', points_in_1
  #CornerCorner
  if len(points_in_1) == 1:
    #print 'CornerCorner: Subdivide', cube1,'at', points_in_1[0]
    cubes = subdivide(cube1, points_in_1[0])
    for cube in cubes:
      #print 'Cube:', cube, is_in(cube2, cube)
      if not is_in(cube2, cube):
        newcubes.append(cube)
    newcubes.append(cube2)
    return newcubes
  #EdgeCorner
  elif len(points_in_1) == 2:
    print 'Side Corner', cube1, cube2
    c1, c2 = points_in_1
    cubes = subdivide_with_2(cube1, c1, c2)
    for cube in cubes:
      #print 'Cube:', cube, is_in(cube2, cube)
      if not is_in(cube2, cube):
        newcubes.append(cube)
    newcubes.append(cube2)
    return newcubes
  #Edge
  #Consule
  return newcubes

class Puzzle:
  def __init__(self):
    self.instructions = []
    self.on = set()

  def process(self, text):
    lines = text.split('\n')
    for line in lines:
      if len(line) > 0:
        self.process_line(line)
    self.process_instructions()

  def process_instructions(self):
    for instruction in self.instructions:
      direction, x1, x2, y1, y2, z1, z2 = instruction
      if direction == 'on':
        self.turn_on(x1, x2, y1, y2, z1, z2)
      else:
        print instruction
        pass
  
  def turn_on(self, x1,x2,y1,y2,z1,z2):
    x = (x1,x2)
    y = (y1,y2)
    z = (z1,z2)
    newcubes = set()
    for cube in self.on:
      if overlap(cube, (x,y,z)):
        #print 'Overlap!'
        cubes = combine(cube, (x,y,z))
        for nc in cubes:
          newcubes.add(nc)
      else:
        newcubes.add(cube)
    #No interactions with any existing cube, add
    newcubes.add((x,y,z))
    self.on = newcubes

  def process_line(self, line):
    direction = 'off'
    if line.startswith('on '):
      direction = 'on'
      line = line.replace('on ', '')
    else:
      line = line.replace('off ', '')
    x, y, z = line.split(',')
    x1, x2 = self.parse_range(x)
    y1, y2 = self.parse_range(y)
    z1, z2 = self.parse_range(z)
    if abs(x1) >50 or abs(x2) > 50 or abs(y1) > 50 or abs(y2) > 50 or abs(z1) > 50 or abs(z2) > 50:
      return
    instruction = (direction, x1, x2, y1, y2, z1, z2)
    self.instructions.append(instruction)

  def count_on(self):
    print 'Sizing', len(self.on), 'cubes'
    total = 0
    for cube in self.on:
      x, y, z = cube
      width  = length(x[0], x[1])
      height = length(y[0], y[1])
      depth  = length(z[0], z[1])
      print cube, width, height, depth, (width * height * depth)
      total += (width * height * depth)
    return total


  def parse_range(self, string):
    string = string[2:]
    left, right = string.split('..')
    return (int(left), int(right))

  def result(self):
    print 'Processed..'
    print self.count_on(), 'Are On'

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

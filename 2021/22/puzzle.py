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

def cleanup(data):
  return filter(lambda d: d != None, data)

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
  x0 = min(x[0], x[1])
  x1 = max(x[0], x[1])
  y0 = min(y[0], y[1])
  y1 = max(y[0], y[1])
  z0 = min(z[0], z[1])
  z1 = max(z[0], z[1])
  for p in points:
    px, py, pz = p
    if px >= x0 and px <= x1 and \
       py >= y0 and py <= y1 and \
       pz >= z0 and pz <= z1:
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

def debug_transpose(cube):
  x, y, z = cube
  return ((x[0], y[0], z[0]), (x[1], y[1], z[1]))

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

def threecut(plane, cube, p1, p2):
  #print '3Cut', plane, p1, p2, 'in', debug_transpose(cube)
  fn = planer_cut_x
  idx = 0
  if plane == 'y':
    fn = planer_cut_y
    idx = 1
  elif plane == 'z':
    fn = planer_cut_z
    idx = 2

  a, right = fn(cube, p1)
  b, c = fn(right, p2+1)
  cmin = min(cube[idx][0], cube[idx][1])
  cmax = max(cube[idx][0], cube[idx][1])
  #print p1, p2, cmin, cmax
  if p1 == cmin: #skip left
    return [None, b, c]
  elif p2 == cmax:
    return [a, b, None]
  return [a,b,c]

def subdivide_with_4(cube, p1, p2, p3, p4):
  #print 'Sub', debug_transpose(cube), p1, p2, p3, p4
  cubes = []
  if p1[0] == p2[0] == p3[0] == p4[0]:
    #X face is inside
    #print 'X face'
    left, right = planer_cut_x(cube, p1[0])
    cubes.append(left)
    minz = min([p1[2], p2[2], p3[2], p4[2]])
    maxz = max([p1[2], p2[2], p3[2], p4[2]])
    miny = min([p1[1], p2[1], p3[1], p4[1]])
    maxy = max([p1[1], p2[1], p3[1], p4[1]])
    a, b, c = threecut('z', right, minz, maxz)
    #print 'A', a, 'B', b, 'C', c
    cubes.append(a)
    cubes.append(c)
    a, b, c = threecut('y', b, miny, maxy)
    #print 'A', a, 'B', b, 'C', c
    cubes.append(a)
    cubes.append(b)
    cubes.append(c)
  elif p1[1] == p2[1] == p3[1] == p4[1]:
    #Y face is inside
    #print 'Y face'
    left, right = planer_cut_y(cube, p1[1])
    cubes.append(left)
    minz = min([p1[2], p2[2], p3[2], p4[2]])
    maxz = max([p1[2], p2[2], p3[2], p4[2]])
    minx = min([p1[0], p2[0], p3[0], p4[0]])
    maxx = max([p1[0], p2[0], p3[0], p4[0]])
    a, b, c = threecut('z', right, minz, maxz)
    #print 'A', a, 'B', b, 'C', c
    cubes.append(a)
    cubes.append(c)
    a, b, c = threecut('x', b, minx, maxx)
    #print 'A', a, 'B', b, 'C', c
    cubes.append(a)
    cubes.append(b)
    cubes.append(c)
  else:
    #Z face is inside
    #print 'Z face'
    left, right = planer_cut_z(cube, p1[2])
    cubes.append(left)
    minx = min([p1[0], p2[0], p3[0], p4[0]])
    maxx = max([p1[0], p2[0], p3[0], p4[0]])
    miny = min([p1[1], p2[1], p3[1], p4[1]])
    maxy = max([p1[1], p2[1], p3[1], p4[1]])
    a, b, c = threecut('x', right, minx, maxx)
    #print 'A', a, 'B', b, 'C', c
    cubes.append(a)
    cubes.append(c)
    a, b, c = threecut('y', b, miny, maxy)
    #print 'A', a, 'B', b, 'C', c
    cubes.append(a)
    cubes.append(b)
    cubes.append(c)
  return cleanup(cubes)

def subdivide_with_2(cube, p1, p2):
  cubes = []
  if p1[0] == p2[0]: #Share X
    left, right = planer_cut_x(cube, p1[0])
    cubes.append(left)
    if p1[1] == p2[1]: #Share XY
      left, right = planer_cut_y(right, p1[1])
      cubes.append(left)
      #Threeway cut Z
      cubes += threecut('z', right, p1[2], p2[2])
    else:  #Share XZ
      left, right = planer_cut_z(right, p1[2])
      cubes.append(left)
      #Threeway cut Y
      cubes += threecut('y', right, p1[1], p2[1])
  elif p1[1] == p2[1]: #Share YZ
    left, right = planer_cut_y(cube, p1[1])
    cubes.append(left)
    left, right = planer_cut_z(right, p1[2])
    cubes.append(left)
    #Threeway cut X
    cubes += threecut('x', right, p1[0], p2[0])
  else:
    print 'Error, Z Not share X, or Y!'
    raise 'Oopsie'
  #print 'CC', cubes
  return cleanup(cubes)

def cut_inside(cube, cutter):
  cubes = []
  x, y, z = cutter
  minx = min([x[0], x[1]])
  maxx = max([x[0], x[1]])
  a, b, c = threecut('x', cube, minx, maxx)
  cubes.append(a)
  cubes.append(c)

  miny = min([y[0], y[1]])
  maxy = max([y[0], y[1]])
  a, b, c = threecut('y', b, miny, maxy)
  cubes.append(a)
  cubes.append(c)

  minz = min([z[0], z[1]])
  maxz = max([z[0], z[1]])
  a, b, c = threecut('z', b, minz, maxz)
  cubes.append(a)
  cubes.append(b)
  cubes.append(c)
  return cleanup(cubes)

def chop_with_4(cube, cutter, p1, p2, p3, p4):
  cubes = []
  if p1[0] == p2[0] == p3[0] == p4[0]:
    #X face is inside
    #print 'X face'
    cx1, cx2 = cutter[0][0], cutter[0][0]
    if cx1 in range(p1[0],p2[0]):
      left, right = planer_cut_x(cube, cx1)
    else:
      left, right = planer_cut_x(cube, cx2)
    cubes.append(left)
  elif p1[1] == p2[1] == p3[1] == p4[1]:
    #Y face is inside
    #print 'Y face'
    cy1, cy2 = cutter[1][0], cutter[1][1]
    if cy1 in range(p1[1],p2[1]):
      left, right = planer_cut_y(cube, cy1)
    else:
      left, right = planer_cut_y(cube, cy2)
    cubes.append(left)
  else:
    #Z face is inside
    #print 'Z face'
    cz1, cz2 = cutter[2][0], cutter[2][1]
    if cz1 in range(p1[2],p2[2]):
      left, right = planer_cut_z(cube, cz1)
    else:
      left, right = planer_cut_z(cube, cz2)
    cubes.append(left)
  return cleanup(cubes)

def chop_with_2(cube, cutter, p1, p2):
  #print 'Chop', debug_transpose(cube), 'with', debug_transpose(cutter), 'Points', p1, p2
  #print cutter
  #print '---'
  cubes = []
  if p1[0] == p2[0]: #Share X
    cx1, cx2 = cutter[0][0], cutter[0][0]
    if cx1 in range(p1[0],p2[0]):
      left, right = planer_cut_x(cube, cx1)
    else:
      left, right = planer_cut_x(cube, cx2)
    cubes.append(left)
    if p1[1] == p2[1]: #Share XY
      cy1, cy2 = cutter[1][0], cutter[1][1]
      if cy1 in range(p1[1],p2[1]):
        left, right = planer_cut_y(right, cy1)
      else:
        left, right = planer_cut_y(right, cy2)
      cubes.append(left)
    else:  #Share XZ
      cz1, cz2 = cutter[2][0], cutter[2][1]
      if cz1 in range(p1[2],p2[2]):
        left, right = planer_cut_z(right, cz1)
      else:
        left, right = planer_cut_z(right, cz2)
      cubes.append(left)
  elif p1[1] == p2[1]: #Share YZ
    cy1, cy2 = cutter[1][0], cutter[1][1]
    if cy1 in range(p1[1],p2[1]):
      left, right = planer_cut_y(cube, cy1)
    else:
      left, right = planer_cut_y(cube, cy2)
    cubes.append(left)
    cz1, cz2 = cutter[2][0], cutter[2][1]
    if cz1 in range(p1[2],p2[2]):
      left, right = planer_cut_z(right, cz1)
    else:
      left, right = planer_cut_z(right, cz2)
    cubes.append(left)
  else:
    print 'Error, Z Not share X, or Y!'
    raise 'Oopsie'
  return cleanup(cubes)
  
def cut(cube1, cutter):
  newcubes = []
  #print cube1, cutter
  corners2 = corners(cutter)
  points_in_1 = pointsin(cube1, corners2)
  #CornerCorner
  if len(points_in_1) == 1:
    cubes = subdivide(cube1, points_in_1[0])
    for cube in cubes:
      if not is_in(cutter, cube):
        newcubes.append(cube)
    return newcubes
  #EdgeCorner
  elif len(points_in_1) == 2:
    c1, c2 = points_in_1
    cubes = subdivide_with_2(cube1, c1, c2)
    for cube in cubes:
      if not is_in(cutter, cube):
        newcubes.append(cube)
    return newcubes
  #Face
  elif len(points_in_1) == 4:
    #print 'Face Overlap', debug_transpose(cube1), debug_transpose(cutter)
    c1, c2, c3, c4 = points_in_1
    cubes = subdivide_with_4(cube1, c1, c2, c3, c4)
    #print 'Face:', cubes
    for cube in cubes:
      #print 'Cube:', cube, is_in(cutter, cube)
      if not is_in(cutter, cube):
        newcubes.append(cube)
    return newcubes
  #Totally Covered
  elif len(points_in_1) == 8:
    cubes = cut_inside(cube1, cutter)
    for cube in cubes:
      if not is_in(cutter, cube):
        newcubes.append(cube)
    return newcubes
  else:
    #The Cube is smaller and cutter points not in
    ccorners = corners(cube1)
    cpoints = pointsin(cutter, ccorners)
    if len(cpoints) == 8:
      #This is a cube totally in cutter?
      #print 'Total Cut?', debug_transpose(cube1), debug_transpose(cutter)
      return []
    elif len(cpoints) == 2:
      #Edge chop  L style
      c1, c2 = cpoints
      cubes = chop_with_2(cube1, cutter, c1, c2)
      for cube in cubes:
        if not is_in(cutter, cube):
          newcubes.append(cube)
      return newcubes
    elif len(cpoints) == 4:
      #Face chop
      c1, c2, c3, c4 = cpoints
      cubes = chop_with_4(cube1, cutter, c1, c2, c3, c4)
      for cube in cubes:
        if not is_in(cutter, cube):
          newcubes.append(cube)
      return newcubes
    else:
      print '===================='
      print 'Cutter', debug_transpose(cutter)
      print 'Cube', cube1
      print 'Points', cpoints
      print '(Other Points)', points_in_1
      print '===================='
      print debug_transpose(cube1)
      print corners(cube1)
      print debug_transpose(cutter)
      print corners(cutter)
      print '===================='
      raise 'Unknown Condition - cutter larger'
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
        self.turn_off(x1, x2, y1, y2, z1, z2)

  def turn_off(self, x1, x2, y1, y2, z1, z2):
    x = (x1,x2)
    y = (y1,y2)
    z = (z1,z2)
    newcubes = set()
    for cube in self.on:
      if overlap(cube, (x,y,z)):
        cubes = cut(cube, (x,y,z))
        for nc in cubes:
          newcubes.add(nc)
      else: #Does not cut this cube
        newcubes.add(cube)
    self.on = newcubes
  
  def turn_on(self, x1,x2,y1,y2,z1,z2):
    x = (x1,x2)
    y = (y1,y2)
    z = (z1,z2)
    newcubes = set()
    for cube in self.on:
      if overlap(cube, (x,y,z)):
        cubes = cut(cube, (x,y,z))
        for nc in cubes:
          newcubes.add(nc)
      else: #Does not cut this cube
        newcubes.add(cube)
    #Finally add cube to set
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
    x0 = min(x1,x2)
    x1 = max(x1,x2)
    y0 = min(y1,y2)
    y1 = max(y1,y2)
    z0 = min(z1,z2)
    z1 = max(z1,z2)

    instruction = (direction, x0, x1, y0, y1, z0, z1)
    self.instructions.append(instruction)

  def count_on(self):
    print 'Sizing', len(self.on), 'cubes'
    total = 0
    for cube in self.on:
      x, y, z = cube
      width  = length(x[0], x[1])
      height = length(y[0], y[1])
      depth  = length(z[0], z[1])
      print debug_transpose(cube), width, height, depth, (width * height * depth)
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

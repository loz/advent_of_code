def intersecting_cuboid(cube1, cube2):
  newcube = [[0,0,0], [0,0,0]]
  for axis in [0, 1, 2]: #x, y, z
    c1 = cube1[0][axis]
    c2 = cube1[1][axis]
    t1 = cube2[0][axis]
    t2 = cube2[1][axis]
    
    #Left of axis bound
    if c1 >= t1 and c1 <= t2:
      newcube[0][axis] = c1
    elif t1 >= c1 and t1 <= c2:
      newcube[0][axis] = t1
    else:
      return None

    #Right of axis bound
    if c2 >= t1 and c2 <= t2:
      newcube[1][axis] = c2
    elif t2 >= c1 and t2 <= c2:
      newcube[1][axis] = t2
    else:
      return None
  p1, p2 = newcube
  x, y, z = p1
  p1 = (x, y, z)
  x, y, z = p2
  p2 = (x, y, z)
  newcube = (p1, p2)

  if newcube == ((0,0,0), (0,0,0)):
    return None
  return newcube

def in2d(points1, points2):
  xs = map(lambda p: p[0], points1)
  ys = map(lambda p: p[1], points1)
  print xs, ys
  x0 = min(xs)
  x1 = max(xs)
  y0 = min(ys)
  y1 = max(ys)
  keep = []
  for p in points2:
    print p
    if p[0] >= x0 and p[0] <= x1 and \
       p[1] >= y0 and p[1] <= y1:
      keep.append(p)
  
  return keep
 
def calc_2d_cuts(cube_xy, cutr_xy):
  points = in2d(cube_xy, cutr_xy)
  print 'CALC:', points
  #return x, y = 

def length(a, b):
  mmin = min(a,b)
  mmax = max(a,b)
  return abs(mmin - (mmax+1))

def cleanup(data):
  clean = []
  #for d in data:
  #  if d != None:
  #    x0 = min(d[0][0], d[0][1])
  #    x1 = max(d[0][0], d[0][1])
  #    y0 = min(d[1][0], d[1][1])
  #    y1 = max(d[1][0], d[1][1])
  #    z0 = min(d[2][0], d[2][1])
  #    z1 = max(d[2][0], d[2][1])
  #    clean.append(((x0,x1), (y0,y1), (z0,z1)))
  #return clean
  return filter(lambda d: d != None, data)

#def is_in(bigger, smaller):
#  small_corners = corners(smaller)
#  in_bigger = pointsin(bigger, small_corners)
#  return len(in_bigger) == 8

def xxx_xy_corners(cube):
  x, y, z = cube
  return [
    (x[0], y[0]),
    (x[0], y[1]),
    (x[1], y[0]),
    (x[1], y[1])
  ]

def xxx_xz_corners(cube):
  x, y, z = cube
  return [
    (x[0], z[0]),
    (x[0], z[1]),
    (x[1], z[0]),
    (x[1], z[1])
  ]

def xxx_yz_corners(cube):
  x, y, z = cube
  return [
    (y[0], z[0]),
    (y[0], z[1]),
    (y[1], z[0]),
    (y[1], z[1])
  ]

def xxx_corners(cube):
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

def xxx_pointsin(cube, points):
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
  p1, p2 = cube
  if x == p1[0]:
    return (None, cube)

  x0 = min([p1[0], p2[0]])
  x1 = max([p1[0], p2[0]])

  return (
    ((x0, p1[1], p1[2]), (x-1, p2[1], p2[2])),
    ((x , p1[1], p1[2]), (x1 , p2[1], p2[2]))
  )

def planer_cut_y(cube, y):
  p1, p2 = cube
  if y == p1[1]:
    return (None, cube)

  y0 = min([p1[1], p2[1]])
  y1 = max([p1[1], p2[1]])

  return (
    ((p1[0], y0, p1[2]), (p2[0], y-1, p2[2])),
    ((p1[0], y , p1[2]), (p2[0], y1 , p2[2]))
  )

def planer_cut_z(cube, z):
  p1, p2 = cube
  if z == p1[2]:
    return (None, cube)

  z0 = min([p1[2], p2[2]])
  z1 = max([p1[2], p2[2]])

  return (
    ((p1[0], p1[1], z0), (p2[0], p2[1], z-1)),
    ((p1[0], p1[1], z ), (p2[0], p2[1], z1 ))
  )

def xxx_debug_transpose(cube):
  x, y, z = cube
  return ((x[0], y[0], z[0]), (x[1], y[1], z[1]))

def xxx_subdivide(cube, point):
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
  #print '3Cut', plane, p1, p2, 'in', cube
  fn = planer_cut_x
  idx = 0
  if plane == 'y':
    fn = planer_cut_y
    idx = 1
  elif plane == 'z':
    fn = planer_cut_z
    idx = 2

  a, right = fn(cube, p1)
  b, c = fn(right, p2)
  #print '---8<----'
  #print a, b, c
  #print '---8<----'
  return [a,b,c]

def xxx_subdivide_with_4(cube, p1, p2, p3, p4):
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
  c1, c2 = cube
  #X Cut
  a, b, c = threecut('x', cube, c1[0], c2[0])
  cubes.append(a)
  cubes.append(c)

  a, b, c = threecut('y', b, c1[1], c2[1])
  cubes.append(a)
  cubes.append(c)

  a, b, c = threecut('z', b, c1[2], c2[2])
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
  print 'Chop', debug_transpose(cube), 'with', debug_transpose(cutter), 'Points', p1, p2
  #print cutter
  #print '---'
  cubes = []
  if p1[0] == p2[0]: #Share X
    if p1[1] ==p2[1]: #Share XY
      print 'Share XY'
      cube_xy = xy_corners(cube)
      cutr_xy = xy_corners(cutter)
      x, y = calc_2d_cuts(cube_xy, cutr_xy)
      print 'X', x, 'Y', y
      pass
    else: #Share XZ
      print 'Share XZ'
      pass
  elif p1[1] == p2[1]: #Share YZ
    print 'Share YZ'
    pass
  else:
    print 'Error, Z Not share X, or Y!'
    raise 'Oopsie'
  return cleanup(cubes)
  
def cut(thecube, cutter):
  newcubes = []
  cubes = cut_inside(thecube, cutter)
  for cube in cubes:
    crop = intersecting_cuboid(cutter, cube)
    print '--', cube, (crop != None)
    if not crop:
      newcubes.append(cube)
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
    #step = 0
    for instruction in self.instructions:
      #step += 1
      #print 'Step', step
      direction, cube = instruction
      self.flip(instruction)

  def flip(self, instruction):
    direction, cube = instruction

    newcubes = set()
    for ecube in self.on:
      ol = intersecting_cuboid(ecube, cube)
      if ol:
        print 'Cube', ecube, 'Vs', cube
        print 'Overlaps', ol
        cubes = cut(ecube, ol)
        for nc in cubes:
          #print '--', nc
          newcubes.add(nc)
      else: #Does not overlap this cube
        newcubes.add(ecube)

    if direction == 'on':
      newcubes.add(cube)

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
    p1 = (x0, y0, z0)
    p2 = (x1, y1, z1)

    instruction = (direction, (p1, p2))
    self.instructions.append(instruction)

  def count_on(self):
    #print 'Sizing', len(self.on), 'cubes'
    total = 0
    for cube in self.on:
      p1, p2 = cube
      width  = length(p1[0], p2[0])
      height = length(p1[1], p2[1])
      depth  = length(p1[2], p2[2])
      #print cube, width, height, depth, (width * height * depth)
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

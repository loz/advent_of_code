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

def planer_cut_x(cube, x):
  p1, p2 = cube
  if x == p1[0]:
    return (None, cube)

  if x > p2[0]:
    return (cube, None)

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

  if y > p2[1]:
    return (cube, None)

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

  if z > p2[2]:
    return (cube, None)

  z0 = min([p1[2], p2[2]])
  z1 = max([p1[2], p2[2]])

  return (
    ((p1[0], p1[1], z0), (p2[0], p2[1], z-1)),
    ((p1[0], p1[1], z ), (p2[0], p2[1], z1 ))
  )

def threecut(plane, cube, p1, p2):
  #print '3Cut', plane, p1, p2, 'in', cube
  fn = planer_cut_x
  if plane == 'y':
    fn = planer_cut_y
  elif plane == 'z':
    fn = planer_cut_z

  a, right = fn(cube, p1)
  b, c = fn(right, p2+1)
  #print '---8<----'
  #print a, b, c
  #print '---8<----'
  return [a,b,c]

def cut_inside(cube, cutter):
  cubes = []
  c1, c2 = cutter

  #X Cut
  a, b, c = threecut('x', cube, c1[0], c2[0])
  cubes.append(a)
  cubes.append(c)

  #Y Cut
  a, b, c = threecut('y', b, c1[1], c2[1])
  cubes.append(a)
  cubes.append(c)

  #Z Cut
  a, b, c = threecut('z', b, c1[2], c2[2])
  cubes.append(a)
  cubes.append(b)
  cubes.append(c)

  return cleanup(cubes)

def cut(thecube, cutter):
  newcubes = []
  cubes = cut_inside(thecube, cutter)
  for cube in cubes:
    crop = cutter == cube
    #print '--', cube, crop
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
        #print 'Cube', ecube, 'Vs', cube
        #print 'Overlaps', ol
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
    #if abs(x1) >50 or abs(x2) > 50 or abs(y1) > 50 or abs(y2) > 50 or abs(z1) > 50 or abs(z2) > 50:
    #  return
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

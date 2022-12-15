import sys
import re

class Puzzle:

  def process(self, text):
    self.left = 0
    self.right = 0
    self.top = 0
    self.bottom = 0
    self.sensors = []
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      info = re.match('Sensor at x=(.+), y=(.+): closest beacon is at x=(.+), y=(.+)',line)
      sx, sy, bx, by = info.groups()
      sx, sy, bx, by = int(sx), int(sy), int(bx), int(by)
      d = self.dist(sx, sy, bx, by)
      self.left = min([sx-d, self.left])
      self.right = max([sx+d, self.right])
      self.top = min([sy-d, self.top])
      self.bottom = max([sy+d, self.bottom])

      self.sensors.append(((sx,sy),(bx,by)))

  def dist(self, ax, ay, bx, by):
    return abs(ax-bx) + abs(ay-by)

  def is_beacon(self, x, y):
    for s in self.sensors:
      sx, sy = s[0]
      bx, by = s[1]
      if (x,y) == (bx, by):
        return True #It's a beacon
      elif (x,y) == (sx,sy):
        return False #It's a sensor
      bd = self.dist(sx, sy, bx, by)
      xd = self.dist(sx, sy, x, y)
      if xd <= bd:
        return False
    return None

  def dump(self):
    objects = {}
    for s in self.sensors:
      objects[s[0]] = 'S'
      objects[s[1]] = 'B'

    for y in range(self.top, self.bottom+1):
      print "%2d " % y, 
      for x in range(self.left, self.right+1):
        if (x,y) in objects.keys():
          sys.stdout.write(objects[(x,y)])
        elif self.is_beacon(x,y) == None:
          sys.stdout.write('.')
        else:
          sys.stdout.write('#')
      print ''

  def calc_edge(self, sensor):
    s, b = sensor
    sx, sy = s
    d = self.dist(sx, sy, b[0], b[1])
    dd = d+1
    points = set()
    for offset in range(dd+1):
      points.add((sx-dd+offset, sy-offset))
      points.add((sx-dd+offset, sy+offset))
      points.add((sx+dd-offset, sy-offset))
      points.add((sx+dd-offset, sy+offset))
    return list(points)

  def result1(self):
    row = 2000000
    count = 0
    for x in range(self.left, self.right):
      ch = self.is_beacon(x,row)
      if ch == None:
        sys.stdout.write('.')
      elif ch == True:
        sys.stdout.write('B')
      else:
        sys.stdout.write('#')
        count += 1
    print count, 'Are not beacon at row', row

  def result_test_perim(self):
    dmin = 0
    dmax = 40
    freq = -1
    perim = self.calc_edge(((20,20),(20,35)))
    for y in range(dmin, dmax+1):
      for x in range(dmin, dmax+1):
        if (x,y) in perim:
          sys.stdout.write('o')
        else:
          sys.stdout.write('.')
      print
    
  def result(self):
    print 'Range Bounds', (self.left, self.top), (self.right, self.bottom)
    dmin = 0
    dmax = 4000000
    #Get all perim coords within the bounds
    possible = set()
    for s in self.sensors:
      print s
      perim = self.calc_edge(s)
      for p in perim:
        if p[0] >= 0 and p[0] <= dmax and p[1] >= 0 and p[1] <= dmax:
          possible.add(p)
    possible = list(possible)
    print 'Search Space of ', len(possible), 'items'
    for item in possible:
      ch = self.is_beacon(item[0], item[1])
      if ch == None:
        freq = (4000000 * item[0]) + item[1]
        print 'Freq', freq
        return

if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

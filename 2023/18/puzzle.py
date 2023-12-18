import sys

MOVES = {
  'R': (1, 0),
  'D': (0, 1),
  'L': (-1,0),
  'U': (0,-1)

}

DMAP = {
  '0': 'R',
  '1': 'D',
  '2': 'L',
  '3': 'U'
}

class Puzzle:

  def process(self, text):
    self.holes = {}
    self.instructions = []
    self.curx = 0
    self.cury = 0
    self.holes[(0,0)] = ('.', '.')
    for line in text.split('\n'):
      self.process_line(line)

  def at(self, x, y):
    return self.holes.get((x,y), None)

  def process_line(self, line):
    if line != '':
      d, n, colour = line.split(' ')
      n = int(n)
      colour = colour[1:-1]
      self.instructions.append((d, n, colour))

  def dig1(self):
    for d, n, colour in self.instructions:
      self.paint(d, n, colour)

  def dig2(self):
    points = [(0, 0)]
    perim = 0
    for d, n, colour in self.instructions:
      loc, dist = self.travel(d, n, colour)
      points.append(loc)
      perim += dist
    return points, perim

  def travel(self, d, num, colour):
    newd = DMAP[colour[-1]]
    newnum = colour[1:-1]
    newnum = int(newnum, 16)
    dx, dy = MOVES[newd]
    #print(newd, newnum)
    self.curx += (dx * newnum)
    self.cury += (dy * newnum)
    return (self.curx, self.cury), newnum

  def paint(self, d, num, colour):
    dx, dy = MOVES[d]
    for n in range(num):
      self.curx += dx
      self.cury += dy
      self.holes[(self.curx, self.cury)] = ('.', '.')
    self.holes[(self.curx, self.cury)] = (d, colour)

  def floodline(self, loc, minx, miny, maxx, maxy):
    spill = []
    x, y = loc
    while self.at(x, y) == None:
      self.holes[(x, y)] = ('f', 'f')
      if self.at(x, y-1) == None:
        spill.append((x, y-1))
      if self.at(x, y+1) == None:
        spill.append((x, y+1))
      x += 1
    x, y = loc
    x -= 1
    while self.at(x, y) == None:
      self.holes[(x, y)] = ('f', 'f')
      if self.at(x, y-1) == None:
        spill.append((x, y-1))
      if self.at(x, y+1) == None:
        spill.append((x, y+1))
      x -= 1
    return spill

  def flood(self, minx, miny, maxx, maxy, loc):
    out = True
    for x in range(minx, maxx+1):
      if self.at(x, miny+1) != None:
        loc = (x+1, miny+1)
        break
    print('Filling at', loc)
    tofill=[loc]
    #deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while(tofill):
      current = tofill.pop(0)
      #print(current)
      spill = self.floodline(current, minx, miny, maxx, maxy)
      tofill += spill

  def result(self):
    self.result2()

  def result2(self):
    print('Digging...')
    points, perimeter = self.dig2()
    total = 0
    for n in range(len(points)-1):
      p1 = points[n]
      p2 = points[n+1]
      x1, y1 = p1
      x2, y2 = p2
      seg = ((x1*y2)-(y1*x2))
      #print(p1, p2, seg)
      total += seg
    total = abs(total)
    area = total // 2
    #print('Area', area, 'Diff', area - 952408144115),
    #print('Perim', perimeter)
    print('Total', area + (perimeter//2) + 1)



  def result1(self):

    self.dig1()
    minx, maxx, miny, maxy = 0, 0, 0, 0
    for x, y in self.holes.keys():
      minx = min(minx, x)
      maxx = max(maxx, x)
      miny = min(miny, y)
      maxy = max(maxy, y)
    print(minx, miny, '->', maxx, maxy)
    self.flood(minx, miny, maxx, maxy, (-1,0))
    count = 0
    for y in range(miny, maxy+1):
      for x in range(minx, maxx+1):
        if (x, y) in self.holes:
          sys.stdout.write('#')
          count += 1
        else:
          sys.stdout.write('.')
      sys.stdout.write('\n')
    print('Total', count)

if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

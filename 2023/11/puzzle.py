import sys
import itertools

class Puzzle:

  def process(self, text):
    self.stars = []
    y = 0
    tlines = text.split('\n')
    w = len(tlines[0])
    h = len(tlines)
    self.vgaps = [n for n in range(w)]
    self.hgaps = [n for n in range(h)]
    for line in tlines:
      self.process_line(line, y)
      y += 1

  def process_line(self, line, y):
    if line != '':
      x = 0
      for ch in line:
        if ch == '#':
          self.stars.append((x,y))
          if x in self.hgaps:
            self.hgaps.remove(x)
          if y in self.vgaps:
           self.vgaps.remove(y)
        x += 1

  def expand(self, stars, byn=2):
    nstars = []
    for s in stars:
      sx, sy = s
      ex = len(list(filter(lambda x: x < sx, self.hgaps)))
      ey = len(list(filter(lambda y: y < sy, self.vgaps)))

      nx, ny = sx + ((byn-1) * ex), sy + ((byn-1) * ey)
      nstars.append((nx, ny))
    return nstars

  def distance(self, a, b):
    sx, sy = a
    ox, oy = b
    return abs(sx-ox) + abs(sy-oy)

  def nearest(self, stars):
    nearest = {}
    for s in stars:
      sx, sy = s
      dist = 9_999_999_999_999_999
      n = None
      for o in stars:
        if s != o:
          ox, oy = o
          d = abs(sx-ox) + abs(sy-oy)
          if d < dist:
            dist = d
            n = o
      nearest[s] = n
          
    return nearest

  def result(self):
    self.result2()

  def result2(self):
    stars = self.expand(self.stars, 1000000)
    total = 0
    pairs = itertools.combinations(stars, 2)
    for s, o in pairs:
      d = self.distance(s, o)
      print(s, o, '->', d)
      total += d
    print('Total', total)

  def result1(self):
    stars = self.expand(self.stars)
    total = 0
    pairs = itertools.combinations(stars, 2)
    for s, o in pairs:
      d = self.distance(s, o)
      print(s, o, '->', d)
      total += d
    print('Total', total)

  def result_x(self):
    stars = self.expand(self.stars)
    nears = self.nearest(stars)
    pairs = []
    seen = []
    for s in stars:
      if s not in seen:
        o = nears[s]
        seen.append(s)
        seen.append(o)
        pairs.append((s, o))
    print('Pairs')
    for p in pairs:
      d = self.distance(p[0], p[1])
      print(p, '->', d)




if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

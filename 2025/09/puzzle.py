import sys
from colorama import Fore
from itertools import combinations

import polygon

class Puzzle:

  def __init__(self):
    self.coords = []
    self.reds = {}
    self.greens = {}

  def process(self, text):
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      x, y = line.split(',')
      x = int(x)
      y = int(y)
      self.reds[(x,y)] = True
      self.coords.append((x,y))

  def valid_rect(self, rect):
    w, h = rect
    for y in h:
      for x in w:
        if (x,y) not in self.reds and (x,y) not in self.greens:
          return False
    return True

  def find_largest_rectangle(self, greens = False):
    maxr = 0
    corners = None
    for pair in combinations(self.coords,2):
      a, b = pair
      w = abs(a[0] - b[0]) + 1
      h = abs(a[1] - b[1]) + 1
      area = w * h
      if area > maxr:
        if greens:
          x1 = min(a[0], b[0])
          x2 = max(a[0], b[0])
          y1 = min(a[1], b[1])
          y2 = max(a[1], b[1])
          w = (x1, x2)
          h = (y1, y2)
          #print((x1,y1), '->', (x2,y2))
          #self.print_debug((w,h))
          iscut = polygon.polygon_cuts_rect((w,h), self.coords)
          if iscut:
            #print('No!')
            pass
          else:
            points = polygon.clip_polygon((w,h), self.coords)
            corners = [(w[0], h[0]), (w[1], h[0]), (w[0], h[1]), (w[1], h[1])]
            #print(points, corners)
            noncorners = list(filter(lambda x: x not in corners, points))
            if len(points) in (4,2) and len(noncorners)  == 0:
              #print('YES!', points)
              maxr = area
              corners = pair
            else:
              #print('No:', points)
              pass
        else:
          maxr = area
          corners = pair

    return maxr, corners

  def fill_green_tiles(self):
    l = len(self.coords)
    pred = self.coords[0]
    for i in range(1,l):
      succ = self.coords[i]
      self._fill_line(pred, succ)
      pred = succ
    succ = self.coords[0]
    self._fill_line(pred, succ)
    #self._flood_fill()

  def _flood_fill(self):
    x, y = polygon.reliable_seed_point(self.coords)
    self._flood(x,y)

  def nbrs(self, loc):
    x, y = loc
    deltas = [(-1,0), (1,0), (0, -1), (0, 1)]
    nbrs = []
    for dx,dy in deltas:
      nbrs.append((x+dx, y+dy))
    return nbrs

  def _flood(self, x, y):
    tovisit = [(x,y)]
    visited = {}

    while len(tovisit) > 0:
      cur = tovisit.pop()
      self.greens[cur] = True
      visited[cur] = True
      nbrs = self.nbrs(cur)
      for n in nbrs:
        if n not in visited:
          if n not in self.coords and n not in self.greens:
            tovisit.append(n)
    

  def _fill_line(self, start, end):
    dy, dx = None, None
    if start[1] == end[1]:
      dy = 0
      if start[0] > end[0]:
        dx = -1
      else:
        dx = 1
    else:
      if start[1] > end[1]:
        dy = -1
      else:
        dy = 1
      dx = 0
    cx, cy = start
    while (cx,cy) != end:
      cx += dx
      cy += dy
      if (cx,cy) != end:
        self.greens[(cx,cy)] = True


  def print_debug(self, rect = None):
    print()
    mx = 0
    my = 0
    for x,y in self.coords:
      if x > mx:
        mx = x
      if y > my:
        my = y

    for y in range(my+2):
      for x in range(mx+2):
        if rect and x in rect[0] and y in rect[1]:
          print(Fore.CYAN + 'O' + Fore.RESET, end='')
        elif (x,y) in self.reds:
          print(Fore.RED + '#' + Fore.RESET, end='')
        elif (x,y) in self.greens:
          print(Fore.GREEN + 'X' + Fore.RESET, end='')
        else:
          print('.', end='')
      print()

  def result1(self):
    size, corners = self.find_largest_rectangle()
    print(corners)
    print(size)

  def result(self):
    self.fill_green_tiles()
    size, corners = self.find_largest_rectangle(True)
    print(corners)
    print(size)


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

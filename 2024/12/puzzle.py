import sys
from colorama import Fore

DELTA = [
  (1, 0),
  (0, 1),
  (-1, 0),
  (0,-1)
]
"""

  ##..##
  #....#
  ......
  #....#
  ##..##
"""
CORNERS = [
  ([(-1, 0), (0,-1)], (-1,-1)), #TL
  ([( 1, 0), (0,-1)], ( 1,-1)), #TR
  ([(-1, 0), (0, 1)], (-1, 1)), #BL
  ([( 1, 0), (0, 1)], ( 1, 1))  #BR
]

class Puzzle:

  def process(self, text):
    self.map = []
    self.regions = {}

    for line in text.split('\n'):
      self.process_line(line)
    self.width = len(self.map[0])
    self.height = len(self.map)
    self.scan_regions()

  def process_line(self, line):
    if line != '':
      self.map.append([ch for ch in line])

  def flood_scan(self, x, y, ch, visited):
    tovisit = [(x,y)]
    region = []
    while tovisit:
      cx, cy = tovisit.pop()
      if (cx,cy) not in visited:
        if self.map[cy][cx] == ch:
          region.append((cx,cy))
          visited[(cx,cy)] = True
          for dx, dy in DELTA:
            nx, ny = cx+dx, cy+dy
            if nx in range(self.width) and ny in range(self.height):
              tovisit.append((nx,ny))
    return region

  def calculate_size(self, region):
    perim = 0
    for x, y in region:
      for dx, dy in DELTA:
        nx, ny = x+dx, y+dy
        if (nx,ny) not in region:
          perim += 1
      
    return len(region), perim

  def calculate_edge(self, region):
    #for row in self.map:
    #  print(''.join(row))

    edges = 0
    corner_count = 0
    for (x,y) in region:
      #print((x,y), ':', end='')
      for corner, single in CORNERS:
        outside = 0
        for dx, dy in corner:
          nx,ny = x+dx, y+dy
          if (nx,ny) not in region:
            outside += 1

        if outside == 2:
          corner_count += 1
        elif outside == 0:
          sx, sy = x+single[0], y+single[1]
          if (sx,sy) not in region:
            corner_count += 1
    return len(region), corner_count

  def scan_regions(self):
    visited = {}
    for y, row in enumerate(self.map):
      for x, ch in enumerate(row):
        if (x,y) not in visited:
          newregion = self.flood_scan(x, y, ch, visited)
          if ch not in self.regions:
            self.regions[ch] = []
          self.regions[ch].append(newregion)

  def at(self, x, y):
    return self.map[y][x]

  def region(self, idx):
    if idx in self.regions:
      return self.regions[idx]
    return []

  def result(self):
    total = 0
    for idx in self.regions:
      print(idx)
      for region in self.regions[idx]:
        area, edges = self.calculate_edge(region)
        cost = area * edges
        total += cost
        print(region, area, edges, ':', cost)
    print('Total Costs:', total)

  def result1(self):
    total = 0
    for idx in self.regions:
      print(idx)
      for region in self.regions[idx]:
        area, perim = self.calculate_size(region)
        cost = area * perim
        total += cost
        print(region, area, perim, ':', cost)
    print('Total Costs:', total)


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

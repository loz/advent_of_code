import sys
from colorama import Fore

class Puzzle:

  def __init__(self):
    self.map = []

  def process(self, text):
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      row = []
      for ch in line:
        row.append(ch)
      self.map.append(row)

  def at(self, x, y):
    return self.map[y][x]

  def get_neighbours(self, x, y):
    deltas = [(0,-1), (0,+1), (-1, 0), (+1,0), (-1,-1), (1,1),(-1,1),(1,-1)]
    nbrs = []
    for d in deltas:
      dx = x + d[0]
      dy = y + d[1]
      #print((x,y), '->', (dx, dy))
      if dx >= 0 and dx < len(self.map[0]):
        if dy >= 0 and dy < len(self.map):
          nbrs.append(((dx,dy), self.map[dy][dx]))
    return nbrs

  def scan_accessible(self):
    accessible = set()
    for y in range(len(self.map)):
      for x in range(len(self.map[y])):
        loc = self.at(x,y)
        if loc == '@':
          nbrs = self.get_neighbours(x, y)
          bails = filter(lambda x: x[1] == '@', nbrs)
          bails = list(bails)
          #print((x,y), nbrs, bails)
          if(len(list(bails)) < 4):
            #for b in bails:
            #  accessible.add(b[0])
            accessible.add((x,y))

    return accessible

  def print_debug(self, markers=[]):
    print()
    print(markers)
    print()
    for y in range(len(self.map)):
      for x in range(len(self.map[y])):
        at = self.at(x,y)
        if (x,y) in markers:
          print(Fore.GREEN + at + Fore.RESET, end='')
        elif at == '@':
          print(Fore.YELLOW + at + Fore.RESET, end='')
        else:
          print(at, end='')
      print()

  def result1(self):
    accessible = self.scan_accessible()
    self.print_debug(accessible)
    print('Total:', len(accessible))

  def result2(self):
    total = 0
    accessible = self.scan_accessible()
    while len(accessible) > 0:
      self.print_debug(accessible)
      print('Removing:', len(accessible))
      for loc in accessible:
        x, y = loc
        self.map[y][x]='.'
      total += len(accessible)
      accessible = self.scan_accessible()
    print('Total Removed:', total)

  def result(self):
    self.result2()


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

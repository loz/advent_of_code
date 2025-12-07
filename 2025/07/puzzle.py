import sys
from colorama import Fore

class Puzzle:

  def __init__(self):
    self.diagram = []

  def process(self, text):
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      row = [ch for ch in line]
      self.diagram.append(row)

  def at(self, x, y):
    return self.diagram[y][x]

  def calculate_splits(self):
    splits = set()
    beams = []
    start = None
    for x in range(len(self.diagram[0])):
      if self.diagram[0][x] == 'S':
        start = (x, 1)
        break
      x += 1
    self.trace_beam([start], splits, beams)
    return splits, beams

  def calculate_universes(self):
    start = None
    cache = {}
    for x in range(len(self.diagram[0])):
      if self.diagram[0][x] == 'S':
        start = (x, 1)
        break
      x += 1
    cache[start] = self.trace_universe(start, cache)
    return cache[start]

  def trace_universe(self, loc, cache, beams=[]):
    if loc in cache:
      return cache[loc]
    
    x, y = loc
    if y == len(self.diagram):
      #self.print_debug(beams)
      return 1
    beams.append(loc)
    ch = self.diagram[y][x]
    if ch == '^':
      left = (x-1, y)
      right = (x+1, y)
      cache[left] = self.trace_universe(left, cache, beams + [left])
      cache[right] = self.trace_universe(right, cache, beams + [right])
      return cache[left] + cache[right]
    elif ch == '.':
      return self.trace_universe((x, y+1), cache, beams)

  def trace_beam(self, tovisit, splits, beams):
    visited = []
    while len(tovisit) > 0:
      x, y = tovisit.pop()
      if (x,y) not in visited:
        visited.append((x,y))
        if y == len(self.diagram):
          pass
        else:
          ch = self.diagram[y][x]
          if ch == '^':
            splits.add((x,y))
            tovisit.append((x-1, y))
            tovisit.append((x+1, y))
          elif ch == '.':
            beams.append((x,y))
            tovisit.append((x,y+1))

  def print_debug(self, beams):
    print()
    for y in range(len(self.diagram)):
      row = self.diagram[y]
      for x in range(len(row)):
        ch = row[x]
        if ch == 'S':
          ch = Fore.GREEN + 'S' + Fore.RESET
        elif ch == '^':
          ch = Fore.RED + '^' + Fore.RESET
        elif (x,y) in beams:
          ch = Fore.CYAN + '|' + Fore.RESET
        
        print(ch, end='')
      print()

  def result2(self):
    count = self.calculate_universes()
    print('Total Universes:', count)

  def result1(self):
    splits, beams = self.calculate_splits()
    self.print_debug(beams)
    print('Total Splits:', len(splits))

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

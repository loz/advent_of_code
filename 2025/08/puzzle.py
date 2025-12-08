import sys
from colorama import Fore
from itertools import combinations

class Puzzle:

  def __init__(self):
    self.coords = []

  def process(self, text):
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      vals = line.split(',')
      x, y, z = vals
      x = int(x)
      y = int(y)
      z = int(z)
      self.coords.append((x,y,z))

  def distance_squared(self, a, b):
    x1, y1, z1 = a
    x2, y2, z2 = b
    return ((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)

  def pair_junctions(self, boxes):
    newboxes = {}
    pairings = combinations(boxes,2)
    for pair in pairings:
      a, b = pair
      ds = self.distance_squared(a, b)
      newboxes[(a,b)] = ds
    return newboxes

  def result1(self):
    circuits = []
    cmaps = {}

    pairs = self.pair_junctions(self.coords)
    print('Total Pairings:', len(pairs))
    spairs = {k: v for k, v in sorted(pairs.items(), key=lambda item: item[1])}

    skeys = list(spairs.keys())
    #skeys = skeys[:1000]
    #skeys = skeys[:10]
    fullpair = None
    for pair in skeys:
      dd = spairs[pair]
      a, b = pair
      if a in cmaps:
        if b in cmaps:
          c1 = cmaps[a]
          c2 = cmaps[b]
          if c1 != c2:
            circuits.remove(c1)
            circuits.remove(c2)
            newc = c1 + c2
            circuits.append(newc)
            for member in newc:
              cmaps[member] = newc
          else:
            pass
        else:
          c = cmaps[a]
          cmaps[b] = c
          c.append(b)
      elif b in cmaps:
        c = cmaps[b]
        cmaps[a] = c
        c.append(a)
      else:
        c = [a, b]
        circuits.append(c)
        cmaps[a] = c
        cmaps[b] = c
      if len(circuits) == 1:
        if len(circuits[0]) == len(self.coords):
          print('Full Circuit!', pair)
          fullpair = pair
          break
    """
    circuits = sorted(circuits, key=lambda x: len(x), reverse=True)
    lthree = circuits[:3]
    #lthree = circuits
    print('There are', len(circuits), 'circuits')
    total = 1
    for c in lthree:
      print(c, '\n =>', Fore.GREEN, len(c), Fore.RESET)
      total *= len(c)
    print('Totals', total)
    """
    print(fullpair)
    a, b = fullpair
    print('Distance', a[0] * b[0])

  def result(self):
    self.result1()


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

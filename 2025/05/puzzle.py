import sys
from colorama import Fore

class Puzzle:
  
  def __init__(self):
    self.ranges = []
    self.ids = []

  def process(self, text):
    ranges = True
    for line in text.split('\n'):
      if line == '':
        ranges = False
        continue
      if ranges:
        self.process_range(line)
      else:
        self.process_ids(line)

  def process_range(self, line):
    left, right = line.split('-')
    left = int(left)
    right = int(right)
    self.ranges.append(range(left, right+1))

  def process_ids(self, line):
    i = int(line)
    self.ids.append(i)

  def isFresh(self, i):
    for r in self.ranges:
      if i in r:
        return True
    return False

  def merge_covered(self, covered, r):
    newcover = []
    newr = r
    for c in covered:
      newc = c
      if newr.start in c:
        if newr.stop-1 in c:
          #print('INSIDE!')
          newr = c
          newc = None
          return list(covered)
        newc = None
        oldr = newr
        newr = range(c.start, r.stop)
        #print('OS', oldr.start, 'in', c, ':', oldr, '=>', newr)
      elif newr.stop-1 in c:
        newc = None
        oldr = newr
        newr = range(newr.start, c.stop)
        #print('OE', newr.stop-1, 'in', c, ':', oldr, '=>', newr)
      elif c.start in r and c.stop-1 in r:
        newc = None
      if newc:
        newcover.append(newc)

    newcover.append(newr)
    return newcover

  def result1(self):
    total = 0
    for i in self.ids:
      fresh = self.isFresh(i)
      #print(i, '=>', fresh)
      if fresh:
        total += 1
    print('Total Fresh', total)

  def result2(self):
    covered = []
    total = 0
    n = 0
    ranges = sorted(self.ranges, key = lambda x: x.start)

    for r in ranges:
      n += 1
      #if n == 5:
      #  exit()
      merged = self.merge_covered(covered, r)
      print(r, covered, '=>', merged)
      covered = merged

    covered = sorted(covered, key = lambda x: x.start)

    for c in covered:
      total += len(c)
      print(c, len(c))
    print('Total Coverage', total)

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

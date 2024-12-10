import sys
from colorama import Fore

DELTAS = [
  (-1, 0),
  ( 1, 0),
  (0, -1),
  (0, 1)
]

class Puzzle:

  def process(self, text):
    self.map = []
    for line in text.split('\n'):
      self.process_line(line)
    self.width = len(self.map[0])
    self.height = len(self.map)

  def process_line(self, line):
    if line != '':
      row = []
      for ch in line:
        row.append(int(ch))
      self.map.append(row)

  def find_trailheads(self):
    heads = []
    for y in range(self.height):
      for x in range(self.width):
        if self.map[y][x] == 0:
          heads.append((x,y))
    return heads

  def find_trails(self, trailhead):
    tovisit = [(trailhead, [])]
    trails = []
    while tovisit:
      current = tovisit.pop()
      #print('Visiting:', current)
      loc, walked = current
      height = self.map[loc[1]][loc[0]]
      if height == 9:
        trails.append(walked + [loc])
      else:
        nbrs = [(loc[0]+dx, loc[1]+dy) for dx, dy in DELTAS]
        #print(height, nbrs)
        for nbr in nbrs:
          if nbr[0] in range(self.width) and nbr[1] in range(self.height):
            nheight = self.map[nbr[1]][nbr[0]]
            if nheight == height + 1:
              tovisit.append((nbr, walked + [loc]))

    return trails

  def result(self):
    total = 0
    heads = self.find_trailheads()
    for head in heads:
      trails = self.find_trails(head)
      print(head, len(trails))
      total += len(trails)
    print('Sum of scores:', total)

  def result1(self):
    total = 0
    heads = self.find_trailheads()
    for head in heads:
      trails = self.find_trails(head)
      peaks = set()
      for trail in trails:
        peaks.add(trail[-1])
      print(head, len(peaks))
      total += len(peaks)
    print('Sum of scores:', total)


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

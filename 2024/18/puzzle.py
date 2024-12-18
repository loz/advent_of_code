import sys
from colorama import Fore

import heapq

NBRS = [
  (-1,0),
  ( 1,0),
  (0,-1),
  (0, 1)
]

class Puzzle:

  def process(self, text):
    self.bytes = []
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      x, y = line.split(',')
      self.bytes.append((int(x),int(y)))

  def fall_bytes(self, count):
    locations = {}
    for byte in self.bytes[:count]:
      locations[byte] = True
    return locations

  def solve(self, width, height, corruption):
    visited = {}
    start = (0,0)
    end = (width, height)
    tovisit = [(0, start, [])]
    heapq.heapify(tovisit)

    while tovisit:
      depth, loc, path = heapq.heappop(tovisit)
      if loc not in visited:
        visited[loc] = True

        if loc == end:
          return path + [loc]

        for dx, dy in NBRS:
          nx, ny = loc[0] + dx, loc[1] + dy
          nloc = (nx,ny)
          if nx in range(width+1) and ny in range(height+1):
            if nloc not in visited and nloc not in corruption:
              tovisit.append((depth+1, (nx,ny), path + [loc]))

  
    #No Path Found
    return None

  def dump_map(self, width, height, corruption, path, blocker=None):
    for y in range(height+1):
      for x in range(width+1):
        if (x,y) == blocker:
          print(Fore.YELLOW + '*' + Fore.RESET, end='')
        elif (x,y) in corruption:
          print(Fore.RED + '#' + Fore.RESET, end='')
        elif (x,y) in path:
          print(Fore.GREEN + 'O' + Fore.RESET, end='')
        else:
          print('.', end='')
      print('')

  def result(self):
    self.result2()

  def result2(self):
    #40, 58
    lwr = 12
    upr = len(self.bytes)
    width , height = 6, 6
    lwr = 1024
    upr = len(self.bytes)
    width , height = 70, 70

    """
    for b in range(lwr, upr+1):
      print('  Trying:', b, end='')
      corruption = self.fall_bytes(b)
      path = self.solve(width,height, corruption)
      if path:
        print('->Possible')
        #self.dump_map(width, height, corruption, path)
      else:
        print('->Not Possible')
        #self.dump_map(width, height, corruption, [], self.bytes[b-1])
        found = (b, self.bytes[b-1])
        break
    """  
    while lwr < upr:
      print('Search Space:', lwr, 'to', upr)
      mid = lwr + ((upr-lwr) // 2)
      print('  Trying:', mid, end='')
      corruption = self.fall_bytes(mid)
      path = self.solve(width,height, corruption)
      if path:
        print('->Possible')
        lwr = mid+1
      else:
        print('->Not Possible')
        upr = mid
    found = lwr, self.bytes[lwr-1]
    
    print('----')
    corruption = self.fall_bytes(found[0]-1)
    blocker = found[1]
    path = self.solve(width,height, corruption)
    self.dump_map(width, height, corruption, path, blocker)
    print('Found Point', blocker)

  def result1(self):
    #corruption = self.fall_bytes(12)
    #path = self.solve(6,6, corruption)
    #self.dump_map(6, 6, corruption, path)
    corruption = self.fall_bytes(1024)
    path = self.solve(70,70, corruption)
    self.dump_map(70,70, corruption, path)
    print('Distance:', len(path)-1) #Do not include start

if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

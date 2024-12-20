import sys
from colorama import Fore

NBRS = [
  (-1, 0),
  ( 1, 0),
  (0, -1),
  (0,  1)
]

class Puzzle:

  def process(self, text):
    self.walls = {}

    for row, line in enumerate(text.split('\n')):
      self.process_line(row, line)
    self.height = row

  def process_line(self, row, line):
    if line != '':
      for col, ch in enumerate(line):
        if ch == '#':
          self.walls[(col, row)] = True
        elif ch == 'S':
          self.start = (col, row)
        elif ch == 'E':
          self.end = (col, row)
      self.width = col+1

  def solve(self):
    visited = {}
    tovisit = [(self.start, [])]
    while tovisit:
      loc, path = tovisit.pop()
      if loc == self.end:
        return path + [loc]

      if loc not in visited:
        visited[loc] = True

        for dx, dy in NBRS:
          nx, ny = loc[0] + dx, loc[1] + dy
          if (nx, ny) not in self.walls:
            tovisit.append( ((nx, ny), path + [loc]) )

    return None

  def reachable(self, t, loc, cache, mappath, path, distance):
    #print('Trying', loc, '@', t)
    visited = set(path[:t])
    tovisit = [(t, loc, 1, visited)]
    cheats = []
    best = {}
    while tovisit:
      ct, cloc, depth, visited = tovisit.pop()
      if cloc not in visited:
        if cloc in mappath:
          pt = mappath[cloc]
          if ct < pt:
            saving = pt-ct
            if (loc, cloc) in best:
              if saving > best[(loc, cloc)]:
                #print('Found A Better Path', loc, '->', cloc, '@', ct, 'v', pt, visited)
                best[(loc, cloc)] = saving
            else:
              #print('Found A Path', loc, '->', cloc, '@', ct, 'v', pt, visited)
              best[(loc, cloc)] = saving

        #Change to if not elif for cutting walls?
        elif depth <= distance:
          #Traverse Neighbours
          for dx, dy in NBRS:
            wx, wy = cloc[0] + dx, cloc[1] + dy
            if (wx, wy) not in visited:
              tovisit.append( (ct+1, (wx, wy), depth+1, visited | set([cloc])) )
    for key in best:
      #print(key, 'saving', cache[key])
      #reachable.append(key[1])
      #CHEAT: (saving, loc, (cx, cy) )
      cheats.append( (best[key], key[0], key[1]) )

    return cheats

  """
    Strategy:
      *For given start, flood fill to depth or return to path
       ?Only interested in return to paths!
        *If at path and better time (startt + depth)!:
          *if depth @ loc < bestdepth[loc]
            *new best depth
      *all cheats are start -> bestdepth indexes
        *startt + cheat depth vs t @ loc is saving
    Optimisations:
      When we have a path (good or bad):
        cache the (best) reachable in N tiles based on reverse
          of path (i.e. in 1 from -1,end, 2 -2, end) etc.
        use cache for path is we already calculated this
  """
  def find_cheats_with_distance(self, path, distance):
    pathmap = {}
    starts = []
    for t, loc in enumerate(path):
      pathmap[loc] = t
      #Add possible cheats to search list
      for dx, dy in NBRS:
        wx, wy = loc[0] + dx, loc[1] + dy
        if (wx, wy) in self.walls:
          starts.append( (t+1, (wx, wy)) )

    cheats = []
    cache = {}
    for t, loc in starts:
      #print('Trying to cheat at:', loc, '@', t)
      cheats += self.reachable(t, loc, cache, pathmap, path, distance)
    return cheats

  def find_cheats(self, path):
    visited = {}
    starts = []
    for t, loc in enumerate(path):
      visited[loc] = t
      #Add possible cheats to search list
      for dx, dy in NBRS:
        wx, wy = loc[0] + dx, loc[1] + dy
        if (wx, wy) in self.walls:
          starts.append( (t+1, (wx, wy)) )

    cheats = []
    for t, loc in starts:
      #print('Trying to cheat at:', loc, '@', t)
      for dx, dy in NBRS:
        cx, cy = loc[0] + dx, loc[1] + dy
        ct = t+1
        if (cx, cy) in visited and visited[(cx,cy)] > ct:
          saving = visited[(cx,cy)]-ct
          #print('Faster! -> saves', saving)
          cheats.append( (saving, loc, (cx, cy) ))
      
    return cheats

  def dump_maze(self, path):
    visits = {}
    for p in path:
      visits[p] = True

    for row in range(self.height):
      for col in range(self.width):
        if (col, row) == self.start:
          print(Fore.CYAN + 'S' + Fore.RESET, end='')
        elif (col, row) == self.end:
          print(Fore.CYAN + 'E' + Fore.RESET, end='')
        elif (col, row) in visits:
          print(Fore.GREEN + 'O' + Fore.RESET, end='')
        elif (col, row) in self.walls:
          print(Fore.RED + '#' + Fore.RESET, end='')
        else:
          print('.', end='')
      print('')


  def result(self):
    self.result2()

  def result2(self):
    frequency = {}
    path = self.solve()
    cheats = self.find_cheats_with_distance(path, 20)
    for cheat in cheats:
      saving, _, _ = cheat
      ctotal = frequency.get(saving, 0)
      ctotal += 1
      frequency[saving] = ctotal
    
    total = 0
    for f in frequency:
      count = frequency[f]
      #print('There are', count, 'saving', f)
      if f >= 100:
        total += count
    print('=> ', total, 'save > 100')
    

  def result1(self):
    frequency = {}
    path = self.solve()
    cheats = self.find_cheats(path)
    for cheat in cheats:
      saving, _, _ = cheat
      ctotal = frequency.get(saving, 0)
      ctotal += 1
      frequency[saving] = ctotal
    
    total = 0
    for f in frequency:
      count = frequency[f]
      #print('There are', count, 'saving', f)
      if f >= 100:
        total += count
    print('=> ', total, 'save > 100')



if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

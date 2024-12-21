import sys
from colorama import Fore

NBRS = [
  (-1, 0),
  ( 1, 0),
  (0, -1),
  (0,  1)
]

#Clamp the bounds of the search space for circle
# values are <-x-> and <-y-> of bounds
# mul by the diamter
CLAMP = {
 (0, -1): (-1, 1, -1, 0), #Upper circle
 (0,  1): (-1, 1,  0, 1), #Lower circle
 (-1, 0): (-1, 0, -1, 1), #Left circle
 ( 1, 0): ( 0, 1, -1, 1), #Right circle
}

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

  def within_radius(self, t, loc, path, distance):
    cheats = []
    #Manhatten radius/witin circle
    x, y = loc
    minx, maxx = x-distance, x+distance
    miny, maxy = y-distance, y+distance
    
    for mx in range(minx, maxx+1):
      for my in range(miny, maxy+1):
        mdist = abs(x-mx) + abs(y-my)      #Distance from loc
        #Within the grid
        #Within the radius
        #Connects to path
        if mx in range(self.width) and \
           my in range(self.height) and \
           mdist <= distance and \
           (mx,my) in path:                
             ptime = path[(mx, my)]
             ctime = t + mdist
             if ctime < ptime:             #Is faster than original 
               #print( loc, '->', (mx, my), '=', ptime, 'v', ctime)
               saving = ptime-ctime
               cheats.append( (saving, loc, (mx, my)) )

    return cheats

  """
    Strategy:
      Run as fast as possible in a straight line
        This is a circle surounding all points possible in time
      if a point on the path is in this circle, we can cheat to it
        (assuming it is a better time)

    Optimization:
      scan all points and see it is in a circle? O(N) calculations
      scan all points in circle and see if on line O(2*4*Distance)
        2*PI*R, PI is 4 in manhatten distance :D
      for small paths, first is best, but we have > 160 points
        in the real map

    Challenges:
      Running left THEN right is totally possible which would
        backtrack over our path (not counted)

    Solution:
      Only look on semi-circle values in direction we moved into wall?
       /-\     /       \ 
        ^   or |<  or  >|  or   v
               \       /       \-/
  """
  def find_cheats_with_distance(self, path, distance):
    pathmap = {}
    starts = []
    for t, loc in enumerate(path):
      pathmap[loc] = t
      starts.append( (t, loc) )

    cheats = []
    for t, loc in starts:
      cheats += self.within_radius(t, loc, pathmap, distance)
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
      saving, start, end = cheat
      ctotal = frequency.get(saving, 0)
      ctotal += 1
      frequency[saving] = ctotal
    
    total = 0
    minsave = 100
    freqs = list(frequency.keys())
    freqs = sorted(freqs)

    for f in freqs:
      count = frequency[f]
      #if f >= 100:
      if f >= minsave:
        print('There are', count, 'saving', f)
        total += count
    print('=> ', total, 'save >', minsave)
    

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

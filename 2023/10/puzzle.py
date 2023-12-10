import sys

class Puzzle:

  def process(self, text):
    self.map = []
    for line in text.split('\n'):
      self.process_line(line)
    self.find_start()
    self.remap_start()

  def find_start(self):
    self.height = len(self.map)
    self.width = len(self.map[0])
    for y in range(self.height):
      for x in range(self.width):
        if self.map[y][x] == 'S':
          self.start = (x, y)

  def infer_moves(self, x, y):
    moves = []
    nl = self.at(x-1, y)
    nr = self.at(x+1, y)
    nu = self.at(x, y-1)
    nd = self.at(x, y+1)
    #print('>>', nl, nr, nu, nd)
    #LR, LD, LU, RD, RU, UD
    if nl in ('-', 'F', 'L'): #Left
      moves.append('L')
      if nr in ('-', '7', 'J'): #Right
        moves.append('R')
      elif nu in ('|', 'F', '7'): #Up
        moves.append('U')
      elif nd in ('|', 'L', 'J'): #Down
        moves.append('D')
      else:
        pass
    elif nr in ('-', '7', 'J'): #Right
      moves.append('R')
      if nd in ('|', 'L', 'J'): #Down
        moves.append('D')
      elif nu in ('|', 'F', '7'): #Up
        moves.append('U')
      else:
        pass
    elif nu in ('|', 'F', '7'): #Up
      moves.append('U')
      if nd in ('|', 'L', 'J'): #Down
        moves.append('D')
      pass

    if(len(moves) != 2):
      print('??>>', nl, nr, nu, nd, moves)
    return moves

  def get_moves(self, x, y):
    MAPPED = {
      '-': ['L', 'R'],
      '|': ['U', 'D'],
      'F': ['R', 'D'],
      'J': ['L', 'U'],
      'L': ['U', 'R'],
      '7': ['L', 'D']
    }
    ch = self.map[y][x]
    return MAPPED[ch]
    

  def remap_start(self):
    x, y = self.start
    moves = self.infer_moves(x,y)
    #print(self.get_moves(x, y))
    if 'L' in moves:
      if 'R' in moves:
        self.map[y][x] = '-'
      elif 'D' in moves:
        self.map[y][x] = '7'
      elif 'U' in moves:
        self.map[y][x] = 'J'
      else:
        raise '??'
      pass
    elif 'R' in moves:
      if 'D' in moves:
        self.map[y][x] = 'F'
      elif 'U' in moves:
        self.map[y][x] = 'L'
      else:
        raise '??'
    elif 'U' in moves:
      if 'D' in moves:
        self.map[y][x] = '|'
      else:
        raise '??'
    else:
      raise '??'

  def trace_loop(self):
    DMAP = {
      'U': ( 0,-1),
      'D': ( 0, 1),
      'L': (-1, 0),
      'R': ( 1, 0)
    }
    FMAP = {
      'U': 'D',
      'D': 'U',
      'L': 'R',
      'R': 'L'
    }
    visited = {}
    path = []
    curx, cury = self.start
    moves = self.get_moves(curx, cury)
    dfrom = moves[0] #Simulate coming from one of the dirs
    while visited.get((curx, cury), False) == False:
      visited[(curx, cury)] = True
      path.append((curx, cury))
      moves = self.get_moves(curx, cury)
      ##DEBUG
      #if len(moves) != 2:
      #  return visited
      #END_DEBUG
      if moves[0] == dfrom:
        dto = moves[1]
      else:
        dto = moves[0]
      #print('F', dfrom, 'T', dto, '->', DMAP[dto])
      ndx, ndy = DMAP[dto]
      nx, ny = curx + ndx, cury + ndy
      curx = nx
      cury = ny
      dfrom = FMAP[dto]
    return path, visited

  def at(self, x, y):
    if x < 0 or y < 0 or x == self.width or y == self.height:
      return None
    return self.map[y][x]

  def process_line(self, line):
    if line != '':
      self.map.append([ch for ch in line])

  def dump_trace(self):
    print('Start', self.start, '=>', self.at(self.start[0], self.start[1]))
    loop, lmap = self.trace_loop()
    for y in range(self.height):
      for x in range(self.width):
        if (x,y) == self.start:
          sys.stdout.write('#')
        elif lmap.get((x,y), False):
          sys.stdout.write('*')
        else:
          sys.stdout.write(self.map[y][x])
      sys.stdout.write('\n')
    return loop

  def result(self):
    self.result2()

  def result2(self):
    regions = []
    for y in range(self.height):
      r = []
      for x in range(self.width):
        r.append('.')
      regions.append(r)

    DMAP = {
      'U': ( 0,-1),
      'D': ( 0, 1),
      'L': (-1, 0),
      'R': ( 1, 0)
    }
    FMAP = {
      'U': 'D',
      'D': 'U',
      'L': 'R',
      'R': 'L'
    }
    PMAP = {
      #From->To : [a cells] [b cells]
      ('U', 'D'): (['R'], ['L']),
      ('D', 'U'): (['L'], ['R']),

      ('L', 'R'): (['U'], ['D']),
      ('R', 'L'): (['D'], ['U']),

      ('L', 'U'): ([], ['R', 'D']),
      ('U', 'L'): (['R', 'D'], []),

      ('D', 'R'): (['U', 'L'], []),
      ('R', 'D'): ([], ['U', 'L']),

      ('L', 'D'): (['U', 'R'], []),
      ('D', 'L'): ([], ['U', 'R']),

      ('U', 'R'): ([], ['L', 'D']),
      ('R', 'U'): (['L', 'D'], []),
    }
    visited = {}
    curx, cury = self.start
    moves = self.get_moves(curx, cury)
    dfrom = moves[0] #Simulate coming from one of the dirs
    while visited.get((curx, cury), False) == False:
      visited[(curx, cury)] = True
      regions[cury][curx] = '*'
      moves = self.get_moves(curx, cury)
      if moves[0] == dfrom:
        dto = moves[1]
      else:
        dto = moves[0]
      #print('F', dfrom, 'T', dto, '->', PMAP[(dfrom, dto)])
      aa, bb = PMAP[(dfrom, dto)]
      #print(aa, bb)
      for a in aa:
        dx, dy = DMAP[a]
        ax = curx + dx
        ay = cury + dy
        #print(ax, ay)
        if regions[ay][ax] == '.':
          regions[ay][ax] = 'a'
      for a in bb:
        dx, dy = DMAP[a]
        ax = curx + dx
        ay = cury + dy
        if regions[ay][ax] == '.':
          regions[ay][ax] = 'b'
      ndx, ndy = DMAP[dto]
      nx, ny = curx + ndx, cury + ndy
      curx = nx
      cury = ny
      dfrom = FMAP[dto]

    #Flood a/b
    done = False
    while(not done):
      done = True
      for y in range(self.height):
        for x in range(self.width):
          ch = regions[y][x]
          if ch == 'a':
            toflood = self.get_blank_neighbours(x, y, regions)
            for n in toflood:
              done = False
              nx, ny = n
              regions[ny][nx] = 'a'
          elif ch == 'b':
            toflood = self.get_blank_neighbours(x, y, regions)
            for n in toflood:
              done = False
              nx, ny = n
              regions[ny][nx] = 'b'
          elif ch == '.': #Still none-flooded cell
            done = False

    acount = 0
    bcount = 0
    for y in range(self.height):
      for x in range(self.width):
        ch = regions[y][x]
        if ch == 'a':
          acount += 1
        elif ch == 'b':
          bcount += 1
        sys.stdout.write(ch)
      sys.stdout.write('\n')
    print('A', acount, 'B', bcount)

  def get_blank_neighbours(self, x, y, regions):
    blank = []
    neighbours = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for n in neighbours:
      dx, dy = n
      nx, ny = x + dx, y + dy
      if nx >= 0 and ny >= 0 and nx < self.width and ny < self.height:
        if regions[ny][nx] == '.':
          blank.append((nx, ny))
    return blank
    
  def result1(self):
    loop = self.dump_trace()
    print(len(loop), len(loop) / 2)



if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

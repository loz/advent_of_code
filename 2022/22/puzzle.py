import sys

DELTAS = [
  (-1, 0),
  ( 1, 0),
  (0, -1),
  (0,  1)
]

BSCORE = {
  '^': 3,
  '<': 2,
  'v': 1,
  '>': 0
}

HLDELTA = {
  '^': '<',
  '<': 'v',
  'v': '>',
  '>': '^'
}
HRDELTA = {
  '^': '>',
  '<': '^',
  'v': '<',
  '>': 'v'
}

class Puzzle:

  def process(self, text):
    self.map = []
    self.moves = []
    donemap = False
    for line in text.split('\n'):
      donemap = self.process_line(line, donemap)
    self.start = self.find_start()
    #Nasty map does not pad!
    self.height = len(self.map)
    self.padmap()
    self.width = len(self.map[0])
  
  def padmap(self):
    maxw = 0
    for y in range(self.height):
      maxw = max(maxw, len(self.map[y]))
    self.width = maxw
    for y in range(self.height):
      if len(self.map[y]) < maxw:
        padded = self.map[y] + (' ' * (maxw-len(self.map[y])))
        self.map[y] = padded

  def find_start(self):
    x = 0
    while self.map[0][x] != '.':
      x += 1
    return ((x,0), '>')

  def move(self):
    loc, heading = self.start
    visited = {loc:heading}
    for mv in self.moves:
      if mv == 'R':
        heading = HRDELTA[heading]
        visited[loc] = heading
      elif mv == 'L':
        heading = HLDELTA[heading]
        visited[loc] = heading
      else:
        if heading == '^':
          fn = self.up
        elif heading == 'v':
          fn = self.down
        elif heading == '<':
          fn = self.left
        else: #>
          fn = self.right
        for r in range(mv):
          nloc = fn(loc[0], loc[1])
          if self.tile_at(nloc[0], nloc[1]) == '#':
            #hit wall
            break
          else:
            loc = nloc
          visited[nloc] = heading
      #print '='*10, mv
      #self.dump(visited)

    return (loc, heading, visited)

  def process_line(self, line, donemap):
    if line != '':
      if not donemap:
        self.map.append(line)
      else:
        self.moves = self.process_moves(line)
    else:
      return True

  def process_moves(self, line):
    moves = []
    curval = 0
    for ch in line:
      if ch == 'R' or ch == 'L':
        moves.append(curval)
        moves.append(ch)
        curval = 0
      else:
        curval *= 10
        curval += int(ch)
    if ch != 'R' and ch != 'L':
      moves.append(curval)
    return moves

  def left(self, x, y):
    row = self.map[y]
    nx = x-1
    if nx < 0:
      nx = self.width-1
    while row[nx] == ' ':
      nx -= 1
      if nx < 0:
        nx = self.width-1

    return (nx, y)

  def right(self, x, y):
    row = self.map[y]
    nx = x + 1
    if nx == self.width:
      nx = 0
    while row[nx] == ' ':
      nx += 1
      if nx == self.width:
        nx = 0
    return (nx, y)

  def up(self, x, y):
    ny = y-1
    if ny == 0:
      ny = self.height-1
    while self.map[ny][x] == ' ':
      ny -= 1
      if ny == 0:
        ny = self.height-1
    return (x, ny)

  def down(self, x, y):
    ny = y+1
    if ny == self.height:
      ny = 0
    while self.map[ny][x] == ' ':
      ny += 1
      if ny == self.height:
        ny = 0
    return (x, ny)

  def xxxneighbours(self, x, y):
    tiles = []
    for d in DELTAS:
      dx, dy = d
      if dy == 0: #L/R
        pass
      else: #U/D
        pass

      nx = x+dx
      ny = y+dy
      if nx >= self.width:
        nx = 0
      if nx < 0:
        nx = self.width

      tiles.append((nx,ny))
    return tiles

  def tile_at(self, x, y):
    ch = self.map[y][x]
    if ch == ' ':
      return None
    else:
      return ch

  def dump(self, visits, loc=(-1,-1)):
    for y in range(self.height):
      for x in range(self.width):
        if (x,y) == loc:
          sys.stdout.write(u"\u001b[36m")
        else:
          sys.stdout.write(u"\u001b[0m")

        if (x,y) in visits.keys():
          sys.stdout.write(visits[(x,y)])
        else:
          sys.stdout.write(self.map[y][x])
      print

  def result(self):
    #for row in self.map:
    #  print len(row)
    #return
    final = self.move()
    #self.dump(final[2], final[0])
    print 'Final Loc', final[0][0]+1, final[0][1]+1
    print 'Bearing', final[1], BSCORE[final[1]]
    loc = final[0]
    print 'Score:', ((loc[1]+1) * 1000) + ((loc[0]+1)*4) + BSCORE[final[1]]



if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

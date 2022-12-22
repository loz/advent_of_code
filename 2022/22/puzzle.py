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
    self.mapcube()
  
  def padmap(self):
    maxw = 0
    for y in range(self.height):
      maxw = max(maxw, len(self.map[y]))
    self.width = maxw
    for y in range(self.height):
      if len(self.map[y]) < maxw:
        padded = self.map[y] + (' ' * (maxw-len(self.map[y])))
        self.map[y] = padded

  def mapcube(self):
    if self.width > self.height:
      self.map_net1()
    else:
      self.map_net2()

  def map_net1(self):
    size = self.width / 4
    movemap = {}
    for y in range(size*3):
      for x in range(size*4):
        loc = (x,y)
        moves = {
          '>': ((x+1,y), '>'),
          '<': ((x-1,y), '<'),
          '^': ((x,y-1), '^'),
          'v': ((x,y+1), 'v')
        }
        movemap[loc] = moves
    #for 1<->2 edges
    for r in range(size):
      x1 = (2*size)+r
      y1 = 0
      x2 = size-1-r
      y2 = size
      #print (x1,y1), '->', (x2,y2)
      movemap[(x1,y1)]['^'] = ((x2, y2), 'v')
      movemap[(x2,y2)]['^'] = ((x1, y1), 'v')
    #for 1<->3 edges
    for r in range(size):
      x1 = (2*size)
      y1 = r
      x2 = size+r
      y2 = size
      #print (x1,y1), '->', (x2,y2)
      movemap[(x1,y1)]['<'] = ((x2, y2), 'v')
      movemap[(x2,y2)]['^'] = ((x1, y1), '>')
    #for 1<->6 edges
    for r in range(size):
      x1 = (3*size)-1
      y1 = r
      x2 = (4*size)-1
      y2 = (3*size)-1-r
      #print (x1,y1), '->', (x2,y2)
      movemap[(x1,y1)]['>'] = ((x2, y2), '<')
      movemap[(x2,y2)]['>'] = ((x1, y1), '<')
    #for 2<->6 edges
    for r in range(size):
      x1 = 0
      y1 = size + r
      x2 = (4*size)-1-r
      y2 = (3*size)-1
      #print (x1,y1), '->', (x2,y2)
      movemap[(x1,y1)]['<'] = ((x2, y2), '^')
      movemap[(x2,y2)]['v'] = ((x1, y1), '>')

    #for 2<->5 edges
    for r in range(size):
      x1 = r
      y1 = (2*size)-1

      x2 = (3*size)-1-r
      y2 = (3*size)-1
      #print (x1,y1), '->', (x2,y2)
      movemap[(x1,y1)]['v'] = ((x2, y2), '^')
      movemap[(x2,y2)]['v'] = ((x1, y1), '^')

    #for 3<->5 edges
    for r in range(size):
      x1 = size + r
      y1 = (2*size)-1

      x2 = (2*size)
      y2 = (3*size)-1-r
      #print (x1,y1), '->', (x2,y2)
      movemap[(x1,y1)]['v'] = ((x2, y2), '>')
      movemap[(x2,y2)]['<'] = ((x1, y1), '^')

    #for 4<->6 edges
    for r in range(size):
      x1 = (3*size)-1
      y1 = size+r

      x2 = (4*size)-1-r
      y2 = (2*size)
      #print (x1,y1), '->', (x2,y2)
      movemap[(x1,y1)]['>'] = ((x2, y2), 'v')
      movemap[(x2,y2)]['^'] = ((x1, y1), '<')

    #print movemap
    self.movemap = movemap

  def map_net2(self):
    size = self.height / 4
    #print 'size', size
    movemap = {}
    for y in range(size*4):
      for x in range(size*3):
        loc = (x,y)
        moves = {
          '>': ((x+1,y), '>'),
          '<': ((x-1,y), '<'),
          '^': ((x,y-1), '^'),
          'v': ((x,y+1), 'v')
        }
        movemap[loc] = moves
    #for 1 ^^ 2
    for r in range(size):
      x1 = size+r
      y1 = 0
      x2 = 0
      y2 = (3*size)+r
      #print (x1,y1), '->', (x2,y2)
      movemap[(x1,y1)]['^'] = ((x2, y2), '>')
      movemap[(x2,y2)]['<'] = ((x1, y1), 'v')
    #for 1 << 3
    for r in range(size):
      x1 = size
      y1 = r
      x2 = 0
      y2 = (3*size)-1-r
      #print (x1,y1), '->', (x2,y2)
      movemap[(x1,y1)]['<'] = ((x2, y2), '>')
      movemap[(x2,y2)]['<'] = ((x1, y1), '>')
    #for 2 >> 5
    for r in range(size):
      x1 = size-1
      y1 = (size*3)+r
      x2 = size+r
      y2 = (3*size)-1
      #print (x1,y1), '->', (x2,y2)
      movemap[(x1,y1)]['>'] = ((x2, y2), '^')
      movemap[(x2,y2)]['v'] = ((x1, y1), '<')
    #for 2 vv 6
    for r in range(size):
      x1 = r
      y1 = (size*4)-1
      x2 = (2*size)+r
      y2 = 0
      #print (x1,y1), '->', (x2,y2)
      movemap[(x1,y1)]['v'] = ((x2, y2), 'v')
      movemap[(x2,y2)]['^'] = ((x1, y1), '^')
    #for 3 ^^ 4
    for r in range(size):
      x1 = r
      y1 = size*2
      x2 = size
      y2 = size+r
      #print (x1,y1), '->', (x2,y2)
      movemap[(x1,y1)]['^'] = ((x2, y2), '>')
      movemap[(x2,y2)]['<'] = ((x1, y1), 'v')
    #for 4 >> 6
    for r in range(size):
      x1 = (size*2)-1
      y1 = size+r
      x2 = (size*2)+r
      y2 = size-1
      #print (x1,y1), '->', (x2,y2)
      movemap[(x1,y1)]['>'] = ((x2, y2), '^')
      movemap[(x2,y2)]['v'] = ((x1, y1), '<')
    #for 5 >> 6
    for r in range(size):
      x1 = (size*2)-1
      y1 = (2*size)+r
      x2 = (size*3)-1
      y2 = size-1-r
      #print (x1,y1), '->', (x2,y2)
      movemap[(x1,y1)]['>'] = ((x2, y2), '<')
      movemap[(x2,y2)]['>'] = ((x1, y1), '<')

    #print movemap
    self.movemap = movemap

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
        print [loc[0],loc[1]], heading, mv
      elif mv == 'L':
        heading = HLDELTA[heading]
        visited[loc] = heading
        print [loc[0],loc[1]], heading, mv
      else:
        for r in range(mv):
          if heading == '^':
            fn = self.up
          elif heading == 'v':
            fn = self.down
          elif heading == '<':
            fn = self.left
          else: #>
            fn = self.right
          nloc, nheading = fn(loc[0], loc[1])
          if self.tile_at(nloc[0], nloc[1]) == '#':
            #hit wall
            break
          else:
            loc = nloc
            heading = nheading
          print [loc[0],loc[1]], heading, mv
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
    return self.movemap[(x,y)]['<']

  def right(self, x, y):
    return self.movemap[(x,y)]['>']

  def up(self, x, y):
    return self.movemap[(x,y)]['^']

  def down(self, x, y):
    return self.movemap[(x,y)]['v']

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

        if visits.get((x,y), False):
          sys.stdout.write(visits[(x,y)])
        else:
          sys.stdout.write(self.map[y][x])
      print

  def result(self):
    #print self.start
    #print self.moves
    #return
    #for row in self.map:
    #  print len(row)
    #return
    final = self.move()
    self.dump(final[2], final[0])
    #for visit in final[2]:
    #  print visit, final[2][visit]
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

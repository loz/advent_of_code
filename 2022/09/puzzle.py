import sys

class Puzzle:
  DELTAS = {
    'U': ( 0, 1),
    'D': ( 0,-1),
    'L': (-1, 0),
    'R': ( 1, 0)
  }

  def process(self, text):
    self.head = (0, 0)
    self.tails = []
    for t in range(9):
      self.tails.append((0,0))
    self.visited = {(0,0):True}
    for line in text.split('\n'):
      self.process_line(line)

  def dump(self, inst):
    print '==', inst, '=='
    print self.tails
    print '=='*10
    for y in range(20):
      cy = (-1 * y) + 10
      for x in range(20):
        cx = x-10
        idx = self.tails.index((cx,cy)) if (cx,cy) in self.tails else None
        if (cx, cy) == self.head:
          sys.stdout.write('H')
        elif idx != None:
          sys.stdout.write(str(idx+1))
        elif (cx, cy) == (0,0):
          sys.stdout.write('s')
        else:
         sys.stdout.write('.')
      print

  def dump_visited(self):
    print '== visits =='
    for y in range(20):
      cy = (-1 * y) + 10
      for x in range(20):
        cx = x-10
        if (cx, cy) in self.visited.keys():
          sys.stdout.write('#')
        elif (cx, cy) == (0,0):
          sys.stdout.write('s')
        else:
         sys.stdout.write('.')
      print


  def process_line(self, line):
    if line != '':
      mdir, mdist = line.split(' ')
      mdist = int(mdist)
      hx, hy = self.head
      dx, dy = self.DELTAS[mdir]
      for m in range(mdist):
        hx += dx
        hy += dy
        fx, fy = hx, hy
        newtails = []
        for tail in self.tails:
          tx, ty = tail
          fx, fy = self.apply_pull(fx, fy, tx, ty)
          newtails.append((fx, fy))
        self.tails = newtails
        self.visited[self.tails[8]] = True
      self.head = (hx, hy)
      #self.dump(line)

  def apply_pull(self, hx, hy, tx, ty):
    tdx = (hx - tx)
    tdy = (hy - ty)
    dx = tdx / abs(tdx) if tdx != 0 else 0
    dy = tdy / abs(tdy) if tdy != 0 else 0
    nx = tx + 0
    ny = ty + 0
    if tdx == 0: #same col
      if abs(tdy) == 2:
        ny += dy
    elif tdy == 0: #same row
      if abs(tdx) == 2:
        nx += dx
    else:
      #diagonal
      if abs(tdy) == 2 or abs(tdx) == 2:
        ny += dy
        nx += dx
    return (nx, ny)


  def result(self):
    self.dump_visited()
    print 'Tail visited', len(self.visited.keys())


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

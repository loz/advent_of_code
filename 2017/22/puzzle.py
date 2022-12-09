import sys

class Virus:
  RMAP = {
    'UP':'RT',
    'RT':'DN',
    'DN':'LT',
    'LT':'UP'
  }
  LMAP = {
    'UP':'LT',
    'RT':'UP',
    'DN':'RT',
    'LT':'DN'
  }
  DELTAS = {
    'UP':( 0,-1),
    'RT':( 1, 0),
    'DN':( 0, 1),
    'LT':(-1, 0)
  }

  def __init__(self):
    self.infections = 0
    self.pos = (0,0)
    self.dir = 'UP'

  def turnRight(self):
    self.dir = self.RMAP[self.dir]

  def turnLeft(self):
    self.dir = self.LMAP[self.dir]

  def move(self):
    x, y = self.pos
    dx, dy = self.DELTAS[self.dir]
    self.pos = (x+dx, y+dy)

class Puzzle:

  def process(self, text):
    self.virus = Virus()
    self.map = {}
    lines = text.split('\n')
    self.height = len(lines) - 1
    self.width = len(lines[0])
    self.xOffset = (self.width / 2)
    self.yOffset = (self.height / 2)
    self.current_line = 0-self.yOffset
    for line in lines:
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      x = 0-self.xOffset
      for ch in line:
        if ch == '#':
          self.map[(x, self.current_line)] = ch
        x += 1
      self.current_line += 1

  def burst(self):
    node = self.nodeAt(self.virus.pos[0], self.virus.pos[1])
    if node:
      self.virus.turnRight()
      del self.map[self.virus.pos]
    else:
      self.virus.turnLeft()
      self.map[self.virus.pos] = '#'
      self.virus.infections += 1
    self.virus.move()

  def dump(self, size):
    yOffset = size / 2
    xOffset = size / 2
    print '-----', self.virus.dir, '-----'
    for y in range(size):
      cy = 0 - yOffset + y
      for x in range(size):
        cx = 0 - xOffset + x
        #print (cx, cy),
        if self.virus.pos == (cx, cy):
          if self.nodeAt(cx, cy):
            sys.stdout.write('\x08[#]')
          else:
            sys.stdout.write('\x08[.]')
        else:
          if self.nodeAt(cx, cy):
            sys.stdout.write('# ')
          else:
            sys.stdout.write('. ')
      print


  def result(self):
    self.dump(11)
    for run in range(10000):
      self.burst()
      #print run
      #self.dump(11)
    self.dump(51)
    print self.virus.infections, 'infections within bursts'

  def nodeAt(self, x, y):
    return self.map.get((x,y), None)

if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

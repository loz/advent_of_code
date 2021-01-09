DELTAS = {
  'n':  ( 0, -1),
  's':  ( 0,  1),
  'nw': (-1,  0),
  'ne': ( 1,  0),
  'sw': (-1,  1),
  'se': ( 1,  1),
}

DELTAS_ODD = {
  'n':  ( 0, -1),
  's':  ( 0,  1),
  'nw': (-1, -1),
  'ne': ( 1, -1),
  'sw': ( -1,  0),
  'se': (  1, 0)
}

class Puzzle:

  def process(self, text):
    self.location = (0,0)
    self.furthest = 0
    lines = text.split('\n')
    for line in lines:
      if line.strip() != '':
        self.process_line(line)

  def process_line(self, line):
    directions = line.split(',')
    for direction in directions:
      self.follow(direction)

  def follow(self, direction):
    x, y = self.location
    if (abs(x) % 2) == 0:
      delta = DELTAS[direction]
    else:
      delta = DELTAS_ODD[direction]
    dx, dy = delta
    x += dx
    y += dy
    self.location = (x, y)
    d = self.distance(self.location)
    if d > self.furthest:
      self.furthest = d

  def distance(self, loc):
    x, y = loc
    x = abs(x)
    y = abs(y)
    return x + (y - (x/2))


  def result(self):
    print 'Path lead to:', self.location
    print 'Distance', self.distance(self.location)
    print 'Furthest:', self.furthest


if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

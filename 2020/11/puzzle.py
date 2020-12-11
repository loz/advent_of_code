# . . .
# . X .
# . . .

DELTAS = [
  (-1, -1),
  (-1,  0),
  (-1,  1),
  ( 1, -1),
  ( 1,  0),
  ( 1,  1),
  ( 0, -1),
  ( 0,  1)
]
class Puzzle:

  def process(self, text):
    self.rows = filter(lambda r: r.strip() != '', text.split('\n'))
    self.width = len(self.rows[0])
    self.height = len(self.rows)

  def neighbours1(self, x, y):
    locs = map(lambda d: (x+d[0], y+d[1]), DELTAS)
    spaces = []
    for loc in locs:
      lx, ly = loc
      if lx >= 0 and lx < self.width and ly >= 0 and ly < self.height:
        spaces.append(self.rows[ly][lx])
    return spaces

  def neighbours(self, x, y):
    locs = map(lambda d: (x+d[0], y+d[1]), DELTAS)
    spaces = []
    for delta in DELTAS:
      dx, dy = delta
      lx = x
      ly = y
      found = False
      while not found:
        lx = lx + dx
        ly = ly + dy
        if lx >= 0 and lx < self.width and ly >= 0 and ly < self.height:
          ch = self.rows[ly][lx]
          if ch == '#' or ch == 'L':
            spaces.append(ch)
            found = True
        else:
          found = True #off map
    return spaces

  def tick(self):
    newrows = []
    for y in range(0,self.height):
      row = ''
      for x in range(0, self.width):
        ch = self.rows[y][x]
        if ch == 'L':
          neighbours = self.neighbours1(x,y)
          occupied = filter(lambda n: n == '#', neighbours)
          if len(occupied) == 0:
            row = row + '#'
          else:
            row = row + ch
        elif ch == '#':
          neighbours = self.neighbours1(x,y)
          occupied = filter(lambda n: n == '#', neighbours)
          if len(occupied) >= 4:
            row = row + 'L'
          else:
            row = row + ch
        else:
          row = row + ch
      newrows.append(row)
    self.rows = newrows

  def tick2(self):
    newrows = []
    for y in range(0,self.height):
      row = ''
      for x in range(0, self.width):
        ch = self.rows[y][x]
        if ch == 'L':
          neighbours = self.neighbours(x,y)
          occupied = filter(lambda n: n == '#', neighbours)
          if len(occupied) == 0:
            row = row + '#'
          else:
            row = row + ch
        elif ch == '#':
          neighbours = self.neighbours(x,y)
          occupied = filter(lambda n: n == '#', neighbours)
          if len(occupied) >= 5:
            row = row + 'L'
          else:
            row = row + ch
        else:
          row = row + ch
      newrows.append(row)
    self.rows = newrows

  def toString(self):
    return '\n'.join(self.rows)

  def occupiedCount(self):
    total = 0
    for y in range(0,self.height):
      for x in range(0, self.width):
        ch = self.rows[y][x]
        if ch == '#':
          total = total + 1
    return total
    

  def result(self):
    print self.toString()
    print ""
    last = self.toString()
    #for i in range(0, 2):
    while True:
      self.tick2()
      new = self.toString()
      if new == last:
        print "Stabilised!"
        print self.occupiedCount(), 'occupied seats'
        exit()
      last = new
      print self.toString()
      print ""


if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

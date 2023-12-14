import sys

class Puzzle:

  def process(self, text):
    self.resethash = text
    self.rows = []
    self.movecache = {}
    for line in text.split('\n'):
      self.process_line(line)
    self.hashmap()

  def hashmap(self):
    rs = [''.join(r) for r in self.rows]
    self.hash = '\n'.join(rs)

  def reset(self):
    self.hash = self.resethash
    self.unhash()
  
  def unhash(self):
    self.rows = []
    for line in self.hash.split('\n'):
      if line != '':
        self.rows.append([ch for ch in line])

  def process_line(self, line):
    if line != '':
      self.rows.append([ch for ch in line])

  def at(self, x, y):
    return self.rows[y][x]

  def rollNorth(self):
    if (self.hash, 'N') in self.movecache:
      h = self.movecache[(self.hash, 'N')]
      self.hash = h
      return True

    for y in range(len(self.rows)):
      r = self.rows[y]
      for x in range(len(r)):
        if r[x] == 'O':
          self.rows[y][x] = '.'
          ny = y
          while(ny >= 0 and self.rows[ny][x] == '.'):
            ny -= 1
          ny += 1
          self.rows[ny][x] = 'O'
    shash = self.hash
    self.hashmap()
    self.movecache[(shash, 'N')] = self.hash

  def rollSouth(self):
    if (self.hash, 'S') in self.movecache:
      h = self.movecache[(self.hash, 'S')]
      self.hash = h
      return True

    maxy = len(self.rows)
    for y in range(len(self.rows)-1, -1, -1):
      r = self.rows[y]
      for x in range(len(r)):
        if r[x] == 'O':
          self.rows[y][x] = '.'
          ny = y
          while(ny < maxy and self.rows[ny][x] == '.'):
            ny += 1
          ny -= 1
          self.rows[ny][x] = 'O'
    shash = self.hash
    self.hashmap()
    self.movecache[(shash, 'S')] = self.hash

  def rollEast(self):
    if (self.hash, 'E') in self.movecache:
      h = self.movecache[(self.hash, 'E')]
      self.hash = h
      return True
    #print('West')
    maxx = len(self.rows[0])
    for y in range(len(self.rows)):
      r = self.rows[y]
      for x in range(maxx-1, -1, -1):
        if r[x] == 'O':
          self.rows[y][x] = '.'
          nx = x
          while(nx < maxx and self.rows[y][nx] == '.'):
            nx += 1
          nx -= 1
          self.rows[y][nx] = 'O'
    shash = self.hash
    self.hashmap()
    self.movecache[(shash, 'E')] = self.hash

  def rollWest(self):
    if (self.hash, 'W') in self.movecache:
      h = self.movecache[(self.hash, 'W')]
      self.hash = h
      return True
    maxx = len(self.rows[0])
    for y in range(len(self.rows)):
      r = self.rows[y]
      for x in range(maxx):
        if r[x] == 'O':
          self.rows[y][x] = '.'
          nx = x
          while(nx >= 0 and self.rows[y][nx] == '.'):
            nx -= 1
          nx += 1
          self.rows[y][nx] = 'O'
    shash = self.hash
    self.hashmap()
    self.movecache[(shash, 'W')] = self.hash

  def dump(self):
    tscore = 0
    mul = len(self.rows)
    print()
    for r in self.rows:
      n = 0
      for ch in r:
        if ch == 'O':
          n += 1
      mn = mul * n
      tscore += mn
      print(''.join(r), mul, '*', n, '=', mn)
      mul -= 1
    print()
    print('Total', tscore)

  def cycle(self):
    n = self.rollNorth()
    w = self.rollWest()
    s = self.rollSouth()
    e = self.rollEast()
    return n and w and s and e

  def result(self):
    self.result2()

  def result2(self):
    wascached = False
    n = 0
    while(not wascached):
     n = n + 1
     wascached = self.cycle()
    print('Cache Cycle after', n)
    init = n
    repeat = 0

    loop = self.hash
    for r in range(n):
      self.cycle()
      if loop == self.hash:
        print('Looped after', r+1)
        repeat = r+1
        break
    start = 1000000000
    start = start - init
    rem = start % repeat
    print('Really only need', init, '+', rem)
    self.reset()
    for n in range(init):
      self.cycle()
    for n in range(rem):
      self.cycle()
    self.unhash()
    self.dump()

  def result1(self):
    self.rollNorth()
    self.dump()


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

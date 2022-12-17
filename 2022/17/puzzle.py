import sys

BLOCKS = [
  ("####", (4,1)),  #block, widthxheight
  (" # \n###\n # ", (3,3)),
  ("  #\n  #\n###", (3,3)),
  ("#\n#\n#\n#", (1, 4)),
  ("##\n##", (2,2))
]



class Puzzle:
  def __init__(self):
    self.reset()

  def reset(self):
    self.falling = 0
    self.pos = (2, 3)
    self.rockface = []
    self.height = 0
    self.seenfloor = [(0,0)]
    self.windpos = 0

  def process(self, text):
    self.wind = []

    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      for ch in line:
        if ch == '>':
          self.wind.append(1)
        else:
          self.wind.append(-1)
 
  def dump(self, offset=-1, window=-1):
    print ""
    for y in range(self.height):
      ry = self.height-1-y
      if ry >=offset and ry < offset+window:
        sys.stdout.write(u"\u001b[36m")
      else:
        sys.stdout.write(u"\u001b[0m")
      row = self.rockface[self.height-1-y]
      sys.stdout.write("%4d " % ry)
      sys.stdout.write('|')
      for r in row:
        if r:
          sys.stdout.write('#')
        else:
          sys.stdout.write('.')
      print '|'
    print "+-------+"

  def rock_at(self, x, y):
    if y >= self.height or y < 0:
      return False
    return self.rockface[y][x]

  def land_rock(self, rx, ry):
    #print "land at", rx, ry
    shape, size = BLOCKS[self.falling]
    #Expand rockface
    while ry+size[1] > self.height:
      self.rockface.append([False, False, False, False, False, False, False])
      self.height += 1
    rows = shape.split('\n')
    oy = ry+size[1]-1
    for y in range(size[1]):
      for x in range(size[0]):
        if rows[y][x] == '#':
          self.rockface[oy-y][rx+x] = True
    self.falling = (self.falling + 1) % 5
    nx = 2
    ny = self.height+3
    self.pos = (nx, ny)

  def can_fall(self, shape, size, rx, ry):
    if ry <= 0: #TODO
      return False
    rows = shape.split('\n')
    oy = ry+size[1]-1
    for y in range(size[1]):
        for x in range(size[0]):
          #print 'Check', (x, y), (rx+x, oy-y-1)
          if rows[y][x] == '#':
            if self.rock_at(rx+x, oy-y-1):
              #print 'Hit Rock'
              return False
    return True
  
  def can_blow(self, shape, size, rx, ry, wind):
    if (rx + wind + size[0]) > 7 or rx + wind < 0:
      return False
    rows = shape.split('\n')
    oy = ry+size[1]-1
    for y in range(size[1]):
        for x in range(size[0]):
          #print 'Check', (x, y), (rx+x, oy-y-1)
          if rows[y][x] == '#':
            if self.rock_at(rx+x+wind, oy-y):
              #print 'Hit Rock'
              return False
    return True
    

  def tick(self):
    didland = False
    shape, size = BLOCKS[self.falling]
    wind = self.wind[self.windpos]
    x, y = self.pos
    nx = x + wind
    if self.can_blow(shape, size, x, y, wind):
      nx = x + wind
    else:
      nx = x
    if self.can_fall(shape, size, nx, y):
      ny = y - 1
      self.pos = (nx, ny)
    else:
      self.land_rock(nx, y)
      didland = True
    self.windpos = (self.windpos + 1) % len(self.wind)
    return didland

  def run(self, count):
    changes = []
    curheight = 0
    for t in range(count):
      while True:
        result = self.tick()
        if result != False:
          break
      changes.append(self.height - curheight)
      curheight = self.height
    return changes

  def runto_height(self, height):
    blocks = 0
    while self.height <= height:
      while True:
        result = self.tick()
        if result != False:
          blocks += 1
          break
    return blocks
    
    
  def window(self, rows, offset, size):
    chunk = ''
    for row in range(size):
      chunk += rows[offset + row]
    return chunk

  def map_rows(self):
    chars = {True: '#', False: '.'}
    rows = []
    for row in self.rockface:
      rows.append(''.join(map(lambda x: chars[x], row)))
    return rows
    
  def result1(self):
    self.run(2022)
    self.dump()
    print self.height

  def result(self):
    count = 10000
    changes = self.run(count)
    window = 2
    found = False
    print changes
    while not found and window < (count / 3):
      window += 1
      print 'Scanning window', window, 'in', count, 'blocks'

      for offset in range(count - (3*window)):
        w1 = changes[offset:offset+window]
        w2 = changes[offset+window:offset+window+window]
        w3 = changes[offset+window+window:offset+window+window+window]
        #print 'Cmp'
        #print w1
        #print w2
        #print w3
        #print '===='
        if w1 == w2 == w3:
          print 'Window Found after', offset, 'repeats increases over', window
          print w1
          found = True
          break
    if not found:
      print 'No window found in', count
      return
    start = changes[0:offset]
    print start, sum(start)
    print 'repeat', w1, sum(w1)

    startcount = sum(start)
    repcount =sum(w1)

    target = 1000000000000
    repeats = (target - offset) / window
    remains = (target - offset) % window
    print 'Has', repeats, 'cycles, plus', remains
    height = startcount + (repeats * repcount)
    extraheight = sum(w1[0:remains])
    print 'Final height', height + extraheight
    

  def result_visual(self):
    count = 2000
    self.run(count)
    window = 6
    mapped = self.map_rows()
    found = False
    while not found and window < (self.height/3):
      window += 1
      print 'Scanning window', window, 'in', self.height, 'rows'
      for offset in range(self.height - (3*window)):
        w1 = self.window(mapped, offset, window)
        w2 = self.window(mapped, offset+window, window)
        w3 = self.window(mapped, offset+window+window, window)
        if w1 == w2 == w3:
          print 'Window Found', offset, window
          found = True
          break
    if not found:
      print 'No window found in', count
      return

    self.dump(offset, window)
    print self.height
    #e.g. Window Found 25 53
    #  25 + (53 * n)
    self.reset()
    landed = self.runto_height(offset)
    self.dump(offset, window)
    print self.height, 'with', landed, 'blocks'

    self.reset()
    landed2 = self.runto_height(offset+window)
    self.dump(offset, window)
    print self.height, 'with', landed2, 'blocks'
    windowcount = landed2-landed
    print 'Repeat adds', windowcount, 'blocks'
    target = 1000000000000
    repeats = (target - landed) / windowcount
    remains = (target - landed) % windowcount
    print 'Has', repeats, 'cycles, plus', remains
    height = offset + (repeats * window)
    curheight = self.height
    self.run(remains+1)
    extraheight = self.height - curheight
    print 'Final height', height + extraheight

  def result2(self):
    #for t in range(2022):
    #for t in range(1000000000000 / 1000000):
    chunk = 100000
    target = 1000000000000 / chunk
    target = 1000
    for t in range(target):
      #for t2 in range(chunk):
      while True:
        result = self.tick()
        if result != False:
          break
      if result == 'Repeat':
        print 'Repeat At:', t, self.height
        #afor x in range(20):
        #  self.tick()
        #self.dump()
        #return
      #print 'Height', self.height

      #while not self.tick():
      #  pass
      #print self.height
    self.dump()




if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

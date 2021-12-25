class Puzzle:
  def __init__(self):
    self.map = {}
    self.height = 0
    self.width = 0

  def at(self, x, y):
    return self.map.get((x,y), '.')

  def process(self, text):
    lines = text.split('\n')
    for line in lines: 
      if len(line) > 0:
        self.process_line(line)

  def debug(self):
    txt = ''
    for y in range(self.height):
      row = ''
      for x in range(self.width):
        row += self.at(x,y)
      txt = txt + row + '\n'
    return txt

  def step(self):
    newmap = {}
    moved = False
    #>> first
    for cuke in self.map:
      x, y = cuke
      if self.map[cuke] == '>':
        nx = x + 1
        if nx == self.width:
          nx = 0
        if (nx,y) not in self.map:
          newmap[(nx,y)] = '>'
          moved = True
        else:
          newmap[cuke] = '>'
      else:
        newmap[cuke] = self.map[cuke]

    self.map = newmap
    newmap = {}

    #vvv next
    for cuke in self.map:
      x, y = cuke
      if self.map[cuke] == 'v':
        ny = y + 1
        if ny == self.height:
          ny = 0
        if (x,ny) not in self.map:
          newmap[(x,ny)] = 'v'
          moved = True
        else:
          newmap[cuke] = 'v'
      else:
        newmap[cuke] = self.map[cuke]

    self.moved = moved
    self.map = newmap

  def process_line(self, line):
    self.height += 1
    self.width = len(line)
    for x in range(self.width):
      ch = line[x]
      if ch != '.':
       self.map[(x,self.height-1)] = ch


  def result(self):
    count = 0
    moved = True
    print 'Step', count
    print self.debug()
    while moved:
    #for _ in range(4):
      count += 1
      self.step()
      print 'Step', count
      print self.debug()
      moved = self.moved

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

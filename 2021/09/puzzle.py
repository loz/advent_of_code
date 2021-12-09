class Puzzle:

  def process(self, text):
    self.map = []
    lines = text.split('\n')
    for line in lines:
      self.process_line(line)
    self.height = len(self.map)
    self.width = len(self.map[0])

  def process_line(self, line):
    if len(line) != 0:
      row = [int(ch) for ch in line]
      self.map.append(row)
      

  def identify_lows(self):
    #print self.map, self.size
    lows = []
    for y in range(self.height):
      for x in range(self.width):
        height = self.map[y][x]
        neighbours = self.neighbours(x,y)
        larger = filter(lambda x: height >= x, neighbours)
        #print height, neighbours, larger
        if len(larger) == 0:
          lows.append(((x,y), height))
    return lows

  def neighbours(self, x, y):
    deltas = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    values = []
    for d in deltas:
      dx, dy = d
      if y + dy >= 0 and y + dy < self.height and x + dx >= 0 and x + dx < self.width:
         values.append(self.map[y+dy][x+dx])
    return values

  def result(self):
    lows = self.identify_lows()
    risk = 0
    for low in lows:
      print low
      xy, h = low
      risk += 1 + h
    print 'Risk', risk

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

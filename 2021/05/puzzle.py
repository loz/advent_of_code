class Puzzle:

  def __init__(self):
    self.map = []
    self.danger = 0
    for y in range(0,1000):
      row = []
      for x in range(0,1000):
        row.append(0)
      self.map.append(row)

  def process(self, text):
    lines = text.split('\n')
    for line in lines:
      self.process_line(line)
    self.calculate_danger()

  def calculate_danger(self):
    for y in range(0,1000):
      for x in range(0, 1000):
        if self.map[y][x] >= 2:
          self.danger += 1

  def process_line(self, line):
    line = line.rstrip()
    if line == '':
      return
    left, right = line.split(' -> ')
    start = self.decode_coord(left)
    end = self.decode_coord(right)
    self.plotline(start,end)

  def plotline(self, start, end):
    #Horizontal
    if start[1] == end[1]:
      y = start[1]
      x1 = min(start[0], end[0])
      x2 = max(start[0], end[0])
      for x in range(x1,x2+1):
        self.map[y][x] += 1
    #Vertical
    elif start[0] == end[0]:
      x = start[0]
      y1 = min(start[1], end[1])
      y2 = max(start[1], end[1])
      for y in range(y1,y2+1):
        self.map[y][x] += 1

  def decode_coord(self, string):
    x, y = string.split(',')
    x = int(x)
    y = int(y)
    return (x,y)

  def to_str(self,size):
    map = ""
    for y in range(0,size):
      row = ""
      for x  in range(0,size):
        if self.map[y][x] == 0:
          row += '.'
        else:
          row += str(self.map[y][x])
      map += row + '\n'
    return map

  def result(self):
    print self.to_str(10)
    print 'Danger Spots:', self.danger

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

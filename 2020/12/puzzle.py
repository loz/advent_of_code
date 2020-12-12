
#90deg turn Right
RBEARINGS = {
    ( 1, 0): ( 0, 1),
    ( 0, 1): (-1, 0),
    (-1, 0): ( 0,-1),
    ( 0,-1): ( 1, 0)
}
LBEARINGS = {
    ( 1, 0): ( 0,-1),
    ( 0, 1): ( 1, 0),
    (-1, 0): ( 0, 1),
    ( 0,-1): (-1, 0)
}

class Puzzle:

  def process(self, text):
    self.x = 0
    self.y = 0
    self.bx = 1
    self.by = 0
    lines = text.split('\n')
    for line in lines:
      if line.strip() != '':
        self.process_line(line)

  def process_line(self, line):
    action = line[0]
    value = int(line[1:])
    if action == 'N':
      self.y -= value
    elif action == 'S':
      self.y += value
    elif action == 'E':
      self.x += value
    elif action == 'W':
      self.x -= value
    elif action == 'F':
      self.x += self.bx * value
      self.y += self.by * value
    elif action == 'B':
      self.x -= self.bx * value
      self.y -= self.by * value
    elif action == 'R':
      n = value / 90
      for i in range(0,n):
        newbearing = RBEARINGS[(self.bx,self.by)]
        self.bx, self.by = newbearing
    elif action == 'L':
      n = value / 90
      for i in range(0,n):
        newbearing = LBEARINGS[(self.bx,self.by)]
        self.bx, self.by = newbearing

  def result(self):
    print self.x, self.y
    print "Distance:", abs(self.x) + abs(self.y)

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

class Puzzle:
  def __init__(self):
    self.on = set()

  def process(self, text):
    lines = text.split('\n')
    for line in lines:
      if len(line) > 0:
        self.process_line(line)

  def process_line(self, line):
    direction = 'off'
    if line.startswith('on '):
      direction = 'on'
      line = line.replace('on ', '')
    else:
      line = line.replace('off ', '')
    x, y, z = line.split(',')
    x1, x2 = self.parse_range(x)
    y1, y2 = self.parse_range(y)
    z1, z2 = self.parse_range(z)
    if abs(x1) >50 or abs(x2) > 50 or abs(y1) > 50 or abs(y2) > 50 or abs(z1) > 50 or abs(z2) > 50:
      return
    if direction == 'on':
      for x in range(x1,x2+1):
        for y in range(y1,y2+1):
          for z in range(z1,z2+1):
            self.on.add((x,y,z))
    else:
      for x in range(x1,x2+1):
        for y in range(y1,y2+1):
          for z in range(z1,z2+1):
            if (x,y,z) in self.on:
              self.on.remove((x,y,z))

  def count_on(self):
    return len(self.on)


  def parse_range(self, string):
    string = string[2:]
    left, right = string.split('..')
    return (int(left), int(right))

  def result(self):
    print 'Processed..'
    print len(self.on), 'Are On'

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

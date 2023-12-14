import sys

class Puzzle:

  def process(self, text):
    self.rows = []
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      self.rows.append([ch for ch in line])

  def at(self, x, y):
    return self.rows[y][x]

  def rollNorth(self):
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

  def result(self):
    self.rollNorth()
    self.dump()
    self.result1()

  def result1(self):
    pass


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

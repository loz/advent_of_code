class Puzzle:

  def process(self, text):
    lines = filter(lambda l: l.strip() != '', text.split('\n'))
    self.locations = map(self.search_line, lines)

  def search_line(self, line):
    minr = 0
    maxr = 127
    minc = 0
    maxc = 7
    for ch in line:
      mid = minr + ((maxr-minr)/2)
      midc = minc + ((maxc-minc)/2)
      print ch, minr, maxr, mid, minc, maxc, midc
      if ch == 'B':
        minr = mid + 1
      elif ch == 'F':
        maxr = mid
      elif ch == 'L':
        maxc = midc
      elif ch == 'R':
        minc = midc + 1
    return (maxr, maxc)

  def result(self):
    seats = {}
    for i in range(0,1024):
      seats[i] = 'empty'
    for loc in self.locations:
      row, col = loc
      id = row * 8 + col
      seats[id] = 'occupied'
    for key in seats:
      print key, seats[key]

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

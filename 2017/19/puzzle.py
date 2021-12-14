class Puzzle:

  def process(self, text):
    self.rows = []
    self.steps = 0
    self.finished = False
    self.letters = []
    self.direction = (0, 1)
    lines = text.split('\n')
    for line in lines:
      self.process_line(line)
    self.loc = (self.rows[0].index('|'),0)
    self.width = len(self.rows[0])
    self.height = len(self.rows)

  def process_line(self, line):
    if len(line) > 0:
      row = [ch for ch in line]
      self.rows.append(row)

  def travel(self):
    x, y = self.loc
    dx, dy = self.direction
    x += dx
    y += dy
    self.steps += 1
    while self.rows[y][x] != '+':
      sym = self.rows[y][x]
      if sym == ' ':
        self.finished = True
        return
      self.steps += 1
      if sym != '|' and sym != '-':
        self.letters.append(sym)
      x += dx
      y += dy
    self.loc = (x, y)
    self.set_new_direction()
    #print self.loc, self.direction

  def set_new_direction(self):
    x, y = self.direction
    back = (0 - x, 0 - y)
    x, y = self.loc
    deltas = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    for d in deltas:
      if d != back:
        dx, dy = d
        xx = x + dx
        yy = y + dy
        if xx >= 0 and xx < self.width and yy >= 0 and yy < self.height and self.rows[yy][xx] != ' ':
          self.direction = d

  def result(self):
    while not self.finished:
      self.travel()
    print ''.join(self.letters)
    print 'Steps', self.steps

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

class Puzzle:

  def process(self, text):
    self.dots = set()
    self.folds = []
    lines = text.split('\n')
    while len(lines[0]) > 0:
      line = lines[0]
      lines = lines[1:]
      self.process_dot(line)
    lines = lines[1:]
    for line in lines:
      self.process_folds(line)
    pass

  def process_dot(self, dot):
    x, y = dot.split(',')
    x = int(x)
    y = int(y)
    self.dots.add((x,y))
 
  def process_folds(self, fold):
    if len(fold) == 0:
      return
    fold = fold.replace('fold along ', '')
    axis, pos = fold.split('=')
    pos = int(pos)
    self.folds.append((axis,pos))

  def fold(self):
    f = self.folds[0]
    axis, pos = f
    if axis == 'y':
      self.fold_y(pos)
    elif axis == 'x':
      self.fold_x(pos)


  def fold_y(self, pos):
    newdots = set()
    for dot in self.dots:
      x, y = dot
      if y > pos:
        y = pos - (y - pos)
      newdots.add((x, y))
    self.dots = newdots

  def fold_x(self, pos):
    newdots = set()
    for dot in self.dots:
      x, y = dot
      if x > pos:
        x = pos - (x - pos)
      newdots.add((x, y))
    self.dots = newdots

  def to_str(self):
    width = max(self.dots, key=lambda n: n[0])[0]
    height = max(self.dots, key=lambda n: n[1])[1]
    paper = []
    for y in range(height+1):
      row = []
      for x in range(width+1):
        row.append('.')
      paper.append(row)
    for dot in self.dots:
      x, y = dot
      paper[y][x] = '#'
    string = ""
    for row in paper:
      string += ''.join(row) + '\n'
    return string

  def result(self):
    self.fold()
    print self.to_str()
    print 'Dots', len(self.dots)

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

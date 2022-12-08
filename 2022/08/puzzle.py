import sys

class Puzzle:

  def process(self, text):
    self.themap = []
    for line in text.split('\n'):
      self.process_line(line)
    self.width = len(self.themap[0])
    self.height = len(self.themap)

  def process_line(self, line):
    if line != '':
      row = [int(ch) for ch in line]
      self.themap.append(row)

  def chart(self, x, y):
    return self.themap[y][x]

  def visible(self, x, y):
    if x == 0 or x == self.width-1:
      return True
    if y == 0 or y == self.height-1:
      return True
    height = self.chart(x,y)

    #UP
    covered = False
    scan = y-1
    while scan >= 0:
      reading = self.chart(x,scan)
      if reading >= height:
        covered = True
      scan -= 1
    if not covered:
      return True 

    #DN
    covered = False
    scan = y+1
    while scan < self.height:
      reading = self.chart(x,scan)
      if reading >= height:
        covered = True
      scan += 1
    if not covered:
      return True 

    #LEFT
    covered = False
    scan = x-1
    while scan >= 0:
      reading = self.chart(scan, y)
      if reading >= height:
        covered = True
      scan -= 1
    if not covered:
      return True 

    #RIGHT
    covered = False
    scan = x+1
    while scan < self.width:
      reading = self.chart(scan, y)
      if reading >= height: 
        covered = True
      scan += 1
    if not covered:
      return True 

    return False

  def score(self, x, y):
    score = 1
    height = self.chart(x, y)
    #UP
    visible = 0
    scan = y-1
    while scan >= 0:
      reading = self.chart(x,scan)
      if reading < height:
        visible +=1
      elif reading >= height:
        visible +=1
        break
      scan -= 1
    #print 'UP:', visible
    score *= visible

    #DN
    visible = 0
    scan = y+1
    while scan < self.height:
      reading = self.chart(x,scan)
      if reading < height:
        visible +=1
      elif reading >= height:
        visible +=1
        break
      scan += 1
    #print 'DN:', visible
    score *= visible

    #LEFT
    visible = 0
    scan = x-1
    while scan >= 0:
      reading = self.chart(scan, y)
      if reading < height:
        visible +=1
      elif reading >= height:
        visible +=1
        break
      scan -= 1
    #print 'LEFT:', visible
    score *= visible

    #RIGHT
    visible = 0
    scan = x+1
    while scan < self.width:
      reading = self.chart(scan, y)
      if reading < height:
        visible +=1
      elif reading >= height:
        visible +=1
        break
      scan += 1
    #print 'RIGHT:', visible
    score *= visible

    return score

  def result1(self):
    total = 0
    for y in range(self.height):
      for x in range(self.width):
        if self.visible(x, y):
          total += 1
    print 'Total Visible', total

  def result(self):
    maxscore = 0
    for y in range(self.height):
      for x in range(self.width):
        score = self.score(x, y)
        if score > maxscore:
          maxscore = score
    print 'Max Score', maxscore


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

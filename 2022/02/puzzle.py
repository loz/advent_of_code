class Puzzle:
  SCOREMAP = {
    #vROCK
    ('A','X') : (1+6,3+0), #RvS:L
    ('A','Y') : (1+3,1+3), #RvR:D
    ('A','Z') : (1+0,2+6), #RvP:W
    
    #vPAPER
    ('B','X') : (2+6,1+0), #PvR:L
    ('B','Y') : (2+3,2+3), #PvP:D
    ('B','Z') : (2+0,3+6), #PvS:W
    
    #vSCISSORS
    ('C','X') : (3+6,2+0), #SvP:L
    ('C','Y') : (3+3,3+3), #SvS:D
    ('C','Z') : (3+0,1+6), #SvR:W
  }

  def process(self, text):
    self.strategy = []
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      left, right = line.split(' ')
      self.strategy.append((left, right))

  def scores(self, index):
    pair = self.strategy[index]
    return self.SCOREMAP[pair]


  def result(self):
    p1, p2 = 0, 0
    for i in range(len(self.strategy)):
      points = self.scores(i)
      print points
      p1 += points[0]
      p2 += points[1]
    print 'P1', p1, 'P2', p2


if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

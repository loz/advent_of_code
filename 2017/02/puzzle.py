import itertools

class Puzzle:

  def process(self, text):
    self.data = []
    lines = text.split('\n')
    for line in lines:
      if line.strip() != '':
        self.data.append(self.parse_line(line))

  def parse_line(self, line):
    return map(lambda n: int(n), line.split())
  
  def checkline(self, dataline):
    a = min(dataline)
    b = max(dataline)
    return b-a

  def checkdivisor(self, dataline):
    pairs = itertools.combinations(dataline, 2)
    for pair in pairs:
      a, b = pair
      if a % b == 0:
        return a/b
      elif b % a == 0:
        return b/a
    return None

  def result(self):
    total = 0
    for line in self.data:
      total += self.checkline(line)
    print 'Checksum Total', total
    total = 0
    for line in self.data:
      total += self.checkdivisor(line)
    print 'Checkdivisior Total', total

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

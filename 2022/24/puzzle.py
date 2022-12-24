import sys
from collections import defaultdict

class Puzzle:

  def process(self, text):
    self.start = (1,0)
    self.height = 0
    self.r_blizards = defaultdict(list)
    self.u_blizards = defaultdict(list)
    self.l_blizards = defaultdict(list)
    self.d_blizards = defaultdict(list)

    for line in text.split('\n'):
      self.process_line(line)
    self.end = (self.width-2, self.height-1)

  def process_line(self, line):
    if line != '':
      self.width = len(line)
      for x in range(self.width):
        if line[x] == '>':
          self.r_blizards[self.height].append(x)
        elif line[x] == '<':
          self.l_blizards[self.height].append(x)
        elif line[x] == '^':
          self.u_blizards[x].append(self.height)
        elif line[x] == 'v':
          self.d_blizards[x].append(self.height)
      self.height+=1

  def blizard_at(self, loc, t=0):
    x, y = loc
    for b in self.r_blizards[y]:
      if ((b-1+t) % (self.width-2))+1 == x:
        return True
    for b in self.l_blizards[y]:
      if ((b-1-t) % (self.width-2))+1 == x:
        return True
    for b in self.u_blizards[x]:
      if ((b-1-t) % (self.height-2))+1 == y:
        return True
    for b in self.d_blizards[x]:
      #height->5, m = 5-2
      #2@2 -> 3 -> 1 = (2-1+2) % m + 1 = 3 % m +1 = 0 + 1
      if ((b-1+t) % (self.height-2))+1 == y:
        return True
    return False

  def result(self):
    pass



if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

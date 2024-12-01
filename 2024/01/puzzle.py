import sys
from colorama import Fore

class Puzzle:

  def process(self, text):
    self.pairs = []
    self.similarities = None
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      a, b = line.split('   ')
      self.pairs.append((int(a), int(b)))

  def pair(self, idx):
    return self.pairs[idx]

  def left_list(self):
    lst = []
    for p in self.pairs:
      lst.append(p[0])
    return lst

  def right_list(self):
    lst = []
    for p in self.pairs:
      lst.append(p[1])
    return lst

  def match_smallest(self):
    left = self.left_list()
    right = self.right_list()
    left = sorted(left)
    right = sorted(right)
    return list(zip(left, right))

  def scan_right(self):
    self.similarities = {}
    for p in self.pairs:
      v = self.similarities.get(p[1], 0)
      v += 1
      self.similarities[p[1]] = v

  def similarity(self, n):
    if self.similarities == None:
      self.scan_right()
    return self.similarities.get(n, 0)

  def result(self):
    left = self.left_list()
    total = 0
    for n in left:
      sim = self.similarity(n)
      print(n, sim, '>', n*sim)
      total += (n*sim)
    print('Total:', total)

  def result1(self):
    total = 0
    for p in self.match_smallest():
      diff = abs(p[0] - p[1])
      print(p, diff)
      total = total + diff
    print('Total: ', total)


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

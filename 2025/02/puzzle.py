import sys
from colorama import Fore

class Puzzle:

  def __init__(self):
    self.ids = []

  def process(self, text):
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      ids = line.split(',')
      for id in ids:
        if id != '':
          self.ids.append(id)

  def scan_invalid(self, idrange):
    invalid = []
    left, right = idrange.split('-')
    left = int(left)
    right = int(right)
    for i in range(left, right+1):
      #print(i)
      st = str(i)
      l = len(st)
      if l % 2 == 0:
        ileft = st[0:l//2]
        iright = st[l//2:]
        #print(ileft,':', iright)
        if ileft == iright:
          invalid.append(i)
    return invalid

  def scan_invalid2(self, idrange):
    invalid = []
    left, right = idrange.split('-')
    left = int(left)
    right = int(right)
    for i in range(left, right+1):
      if self.is_invalid(i):
        invalid.append(i)
    return invalid

  def is_invalid(self, n):
      st = str(n)
      l = len(st)
      h = l // 2
      #print(n, h)
      for r in range(1,h+1):
        rep = l // r
        seq = st[0:r] * rep
        #print(r, 'v', l, rep, seq)
        if seq == st:
          return True

      return False


  def result1(self):
    total = 0
    for i in self.ids:
      invalid = self.scan_invalid(i)
      print('-', i, invalid)
      for v in invalid:
        total += v
    print('Total', total)

  def result2(self):
    total = 0
    for i in self.ids:
      invalid = self.scan_invalid2(i)
      print('-', i, invalid)
      for v in invalid:
        total += v
    print('Total', total)

  def result(self):
    self.result2()


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

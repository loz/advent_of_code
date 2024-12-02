import sys
from colorama import Fore

class Puzzle:

  def process(self, text):
    self.lists = []
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      nums = line.split(' ')
      self.lists.append([int(n) for n in nums])
  
  def list(self, idx):
    return self.lists[idx]

  def safe(self, tlist):
    ds = []
    d = tlist[0]
    for i in range(1, len(tlist)):
      ds.append(tlist[i]-d)
      d = tlist[i]

    if ds[0] < 0:
      for d in ds:
         if d > 0:
            return False
    elif ds[0] > 0:
      for d in ds:
         if d < 0:
            return False

    for d in ds:
      if d == 0:
         return False
      elif abs(d) > 3:
         return False
    return True

  def tolerable(self, tlist):
     if self.safe(tlist):
        return True
     for i in range(1, len(tlist)+1):
       before = tlist[0:i-1]
       after = tlist[i:]
       test = before + after
       if self.safe(test):
         return True
     return False

  def result(self):
     total = 0
     for l in self.lists:
       issafe = self.tolerable(l)
       print(l, issafe)
       if issafe:
         total += 1
     print('Total:', total)

  def result1(self):
     total = 0
     for l in self.lists:
       issafe = self.safe(l)
       print(l, issafe)
       if issafe:
         total += 1
     print('Total:', total)


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

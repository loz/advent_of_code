import sys
from colorama import Fore

class Puzzle:

  def __init__(self):
    self.batteries = []

  def process(self, text):
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      self.batteries.append(line)

  def find_n_joltage(self, bank, n):
    joltage = 0
    idx = -1
    for dn in range(n):
      offset = n-dn-1
      maxb = 0
      for i in range(idx+1, len(bank)-offset):
        b = bank[i]
        if int(b) > maxb:
          newidx = i
          maxb = int(b)
        #print(idx, offset, b, '=>', maxb, '==', joltage)
      joltage = (joltage * 10) + maxb
      idx = newidx
    return joltage

  def find_joltage(self, bank):
   max1 = 0
   idx1 = -1
   max2 = 0
   for i in range(len(bank)-1):
    b = bank[i]
    if int(b) > max1:
      max1 = int(b)
      idx1 = i

   for i in range(idx1+1, len(bank)):
     b = bank[i]
     if int(b) > max2:
       max2 = int(b)
  
   return max1 * 10 + max2


  def result(self):
    total = 0
    for bat in self.batteries:
      largest = self.find_n_joltage(bat,12)
      print(bat, largest)
      total += largest
    print('Total output:', total)

  def result1(self):
    total = 0
    for bat in self.batteries:
      largest = self.find_joltage(bat)
      print(bat, largest)
      total += largest
    print('Total output:', total)


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

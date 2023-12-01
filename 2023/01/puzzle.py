import sys
import re

class Puzzle:

  def process(self, text):
    self.total = 0
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      pass
    digits = line.replace('one', 'o1e')
    digits = digits.replace('two', 't2o')
    digits = digits.replace('three', 't3e')
    digits = digits.replace('four', 'f4r')
    digits = digits.replace('five', 'f5e')
    digits = digits.replace('six', 's6x')
    digits = digits.replace('seven', 's7n')
    digits = digits.replace('eight', 'e8t')
    digits = digits.replace('nine', 'n9e')
    digits = digits.replace('zero', 'z0o')
    digits = re.sub(r'[^0-9]', '', digits)
    if len(digits) == 0:
      return
    d1 = digits[0]
    d2 = digits[len(digits)-1]
    val = int(d1+d2)
    print(val)
    self.total += val

  def result(self):
    print('Total', self.total)



if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

import sys
from colorama import Fore
import re

class Puzzle:

  def process(self, text):
    self.instructions = []
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      self.parse_instructions(line)
  
  def parse_instructions(self, line):
    p = re.compile(r'((mul|do|don\'t)\(((\d+),(\d+)){0,1}\))')
    #p = re.compile(r'((mul)\((\d+),(\d+)\)|(do)\(\)|(don\'t)\(\))')
    matches = p.findall(line)
    for match in matches:
       inst = match[1]
       a, b = None, None
       if inst == 'mul':
          a = int(match[3])
          b = int(match[4])
       #elif inst == 'do' or inst == "don't":
       #   a = 0
       #   b = 0
       self.instructions.append((inst, a, b))

  def result(self):
    total = 0
    enabled = True
    for i in self.instructions:
       inst, a, b = i
       if inst == 'mul':
         if enabled:
            m = a * b
            print(i, m)
            total += m
         else:
            print(i, m, '<disabled>')
       elif inst == 'do':
         print('<enable>')
         enabled = True
       else: #dont
         print('<disable>')
         enabled = False
    print('Total:', total)

  def result1(self):
    total = 0
    for i in self.instructions:
       m = i[1] * i[2]
       print(i, m)
       total += m
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

import sys
from colorama import Fore

class Puzzle:

  def process(self, text):
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      pass

  def result(self):
    pass



if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
[32mProcessing: [33minput.3[39m...
Traceback (most recent call last):
  File "/Users/jonathan.lozinski/Development/advent_of_code/2024/template.py/puzzle.py", line 25, in <module>
    inp = open(inputfile, 'r').read()
FileNotFoundError: [Errno 2] No such file or directory: 'input.3'

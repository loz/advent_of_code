import sys

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
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

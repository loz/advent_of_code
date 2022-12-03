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
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

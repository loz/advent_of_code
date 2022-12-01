class Puzzle:

  def process(self, text):
    pass

  def result(self):
    pass

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

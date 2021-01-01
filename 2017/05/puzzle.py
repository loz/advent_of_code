class Puzzle:

  def process(self, text):
    self.ip = 0
    self.jumps = []
    lines = text.split('\n')
    for line in lines:
      if line.strip() != '':
        self.jumps.append(int(line))
      

  def execute(self):
    runlength = 0
    while self.ip < len(self.jumps):
      runlength += 1
      jmp = self.jumps[self.ip]
      if jmp >= 3:
        self.jumps[self.ip] -= 1
      else:
        self.jumps[self.ip] += 1
      self.ip += jmp
    return runlength

  def result(self):
    length = self.execute()
    print 'Runlength:', length

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

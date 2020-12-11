class Puzzle:

  def process(self, text):
    self.reg = {'a':0, 'b':0, 'c':0, 'd':0}
    lines = filter(lambda l: l.strip() != '', text.split('\n'))
    self.instructions = map(lambda l: self.parse_line(l), lines)
    self.ip = 0

  def result(self):
    self.reg['c'] = 1
    self.run()
    print self.reg

  def run(self):
    while self.ip < len(self.instructions):
      current = self.instructions[self.ip]
      op = current[0]
      if op == 'cpy':
        val = current[1]
        if val in ['a','b','c','d']:
          val = self.reg[val]
        else:
          val = int(val)
        dest = current[2]
        self.reg[dest] = val
      elif op == 'inc':
        dest = current[1]
        self.reg[dest] = self.reg[dest] + 1
      elif op == 'dec':
        dest = current[1]
        self.reg[dest] = self.reg[dest] - 1
      elif op == 'jnz':
        cmp = current[1]
        offset = int(current[2])
        if cmp in ['a','b','c','d']:
          if self.reg[cmp] != 0:
            self.ip = self.ip + offset -1
        else:
          if int(cmp) != 0:
            self.ip = self.ip + offset -1

      else:
        print "Unknown Op", op
      self.ip = self.ip + 1


  def parse_line(self, line):
    return line.split(' ')

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

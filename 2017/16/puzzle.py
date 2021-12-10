class Puzzle:

  def process(self, text):
    self.programs = 'abcdefghijklmnop'
    ops = text.rstrip().split(',')
    for op in ops:
      self.process_op(op)

  def process_op(self, op):
    if len(op) > 0:
      code = op[0]
      rest = op[1:]
      print code, rest, self.programs
      if code == 's':
        size = int(rest)
        left = self.programs[:-size]
        right = self.programs[-size:]
        self.programs = right + left
      elif code == 'x':
        l, r = rest.split('/')
        l = int(l)
        r = int(r)
        s = [ch for ch in self.programs]
        dst = s[r]
        src = s[l]
        s[l] = dst
        s[r] = src
        self.programs = ''.join(s)
      elif code == 'p':
        l, r = rest.split('/')
        s = [ch for ch in self.programs]
        l = s.index(l)
        r = s.index(r)
        dst = s[r]
        src = s[l]
        s[l] = dst
        s[r] = src
        self.programs = ''.join(s)
        
      pass

  def result(self):
    print self.programs

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

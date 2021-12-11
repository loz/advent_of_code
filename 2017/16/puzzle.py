class Puzzle:

  def process(self, text):
    self.programs = 'abcdefghijklmnop'
    self.ops = text.rstrip().split(',')

  def dance(self, ops):
    for op in ops:
      self.process_op(op)

  def process_op(self, op):
    if len(op) > 0:
      code = op[0]
      rest = op[1:]
      #print code, rest, self.programs
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
    seen = {}
    self.programs = 'abcdefghijklmnop'
    for i in range(1000):
      self.dance(self.ops)
      if seen.get(self.programs, False):
        print 'Repeat! @', i
        oneb = 1000000000 % i
        print '1B same as ', oneb
        self.programs = 'abcdefghijklmnop'
        for i in range(oneb):
          self.dance(self.ops)
        print '=>', self.programs
        return
      else:
        seen[self.programs] = True
      print self.programs

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

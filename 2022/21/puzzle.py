import sys

class Puzzle:

  def process(self, text):
    self.tree = {}
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      key, chunk = line.split(': ')
      try:
        val = int(chunk)
      except:
        left, op, right = chunk.split(' ')
        self.tree[key] = (op, left, right)
      else:
        self.tree[key] = ('int', val)


  def result1(self):
    print 'Root', self.eval('root')

  def result_bin_src(self):
    _, left, right = self.tree['root']
    hmax = 100000000000000
    hmin = 0
    rval = self.eval(right)
    maxloop = 0
    while hmin < (hmax-1):
      maxloop += 1
      h = hmin + ((hmax-hmin)/2)
      print h, '->', #, (hmin, hmax), '->',
      l = self.eval(left, h)
      #rval = self.eval(right, h)
      if l == rval:
        print 'Match when h=', h
        return
      elif l > rval:
        print '>, use uppr', l, 'v', rval
        hmin = h
      else:
        print '<, use lowr', l, 'v', rval
        hmax = h

  def result(self):
    _, left, right = self.tree['root']
    hmax = 100000000000000
    hmax = 3441198826073
    hmin = 0
    rval = self.eval(right)
    maxloop = 0
    while hmin < (hmax-1):
      maxloop += 1
      h = hmin + ((hmax-hmin)/2)
      print h, '->', #, (hmin, hmax), '->',
      l = self.eval(left, h)
      rval = self.eval(right, h)
      if l == rval:
        print 'Match when h=', h
        return
      elif l > rval:
        print '>, use uppr', l, 'v', rval
        hmin = h
      else:
        print '<, use lowr', l, 'v', rval
        hmax = h
    

  def eval(self, node, hmn=None):
    if node == 'humn' and hmn != None:
      return hmn
    action = self.tree[node]
    if action[0] == 'int':
      return action[1]
    elif action[0] == '+':
      return self.eval(action[1],hmn) + self.eval(action[2],hmn)
    elif action[0] == '-':
      return self.eval(action[1],hmn) - self.eval(action[2],hmn)
    elif action[0] == '*':
      return self.eval(action[1],hmn) * self.eval(action[2],hmn)
    elif action[0] == '/':
      return self.eval(action[1],hmn) / self.eval(action[2],hmn)



if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

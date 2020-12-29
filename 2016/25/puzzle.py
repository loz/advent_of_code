import copy
class Puzzle:

  def process(self, text):
    self.reg = {'a':0, 'b':0, 'c':0, 'd':0}
    lines = filter(lambda l: l.strip() != '', text.split('\n'))
    self.instructions = map(lambda l: self.parse_line(l), lines)
    self.ip = 0

  def result(self):
    original = copy.deepcopy(self.instructions)
    for i in range(191, 1000):
      self.instructions = copy.deepcopy(original)
      self.ip = 0
      self.reg = self.reg = {'a':i, 'b':0, 'c':0, 'd':0}
      out = self.run(100000)
      print i, out

  def toggle(self, ptr):
    if ptr < len(self.instructions):
      target_instruction = self.instructions[ptr]
      top = target_instruction[0]
      if top == 'tgl' or top == 'dec':
        target_instruction[0] = 'inc'
      elif top == 'inc':
        target_instruction[0] = 'dec'
      elif top == 'cpy':
        target_instruction[0] = 'jnz'
      elif top == 'jnz':
        target_instruction[0] = 'cpy'
      else:
        print '??Toggle', target_instruction
      self.instructions[ptr] = target_instruction
      #print '??Toggle', target_instruction
    
  def execute(self, out = []): 
    current = self.instructions[self.ip]
    #print self.reg, self.ip, current
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
      offset = current[2]
      if offset in ['a', 'b', 'c', 'd']:
        offset = self.reg[offset]
      offset = int(offset)
      if cmp in ['a','b','c','d']:
        if self.reg[cmp] != 0:
          self.ip = self.ip + offset -1
      else:
        if int(cmp) != 0:
          self.ip = self.ip + offset -1
    elif op == 'out':
      val = current[1]
      if val in ['a','b','c','d']:
        val = self.reg[val]
      else:
        val = int(val)
      out.append(val)
    elif op == 'tgl':
      target = current[1]
      if target in ['a','b','c','d']:
        offset = self.reg[target]
      else:
        offset = int(target)
      ptr = self.ip + offset
      self.toggle(ptr)
    else:
      print "Unknown Op", op
    self.ip = self.ip + 1
    return out

  def run(self, count=None):
    output = []
    if count == None:
      while self.ip < len(self.instructions):
        output = self.execute(output)
    else:
      for i in range(count):
        output = self.execute(output)
    return output

  def parse_line(self, line):
    return line.split(' ')

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

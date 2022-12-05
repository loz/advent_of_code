import textwrap

class Puzzle:

  def process(self, text):
    self.current = 0
    self.numstacks = 0
    self.stacks = [[]]
    self.moves = []
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      if not self.pull_blocks(line):
        self.pull_moves(line)

  def chunk_parts(self, line):
    parts = []
    for i in range(0,len(line), 4):
      part = line[i:i+4]
      part = part.strip()
      if part == '':
        parts.append(None)
      else:
        parts.append(part)
    return parts

  def pull_blocks(self, line):
    parts = self.chunk_parts(line)
    for i in range(0, len(parts)):
      part = parts[i]
      if part == None: #Space
        pass
      elif part.startswith('['):
        if i > self.numstacks:
          self.numstacks += 1
          self.stacks.append([])
        letter = part.replace('[', '').replace(']','')
        self.stacks[i].insert(0, letter)
      else:
        return False
    return True

  def pull_moves(self, line):
    if line.startswith('move'):
      parts = line.split(' ')
      count = int(parts[1])
      cfrom = int(parts[3])
      cto   = int(parts[5])
      self.moves.append((count,cfrom,cto))

  def execute(self):
    if self.current == len(self.moves):
      return False
    move = self.moves[self.current]
    count, cfrom, cto = move
    print 'move', count, 'from', cfrom, 'to', cto
    for b in range(count):
      blk = self.stacks[cfrom-1].pop()
      self.stacks[cto-1].append(blk)
    self.current+=1
    return True

  def dump_stacks(self):
    code = ""
    for stack in self.stacks:
      print stack
      if len(stack) != 0:
        code += stack[len(stack)-1]
    print 'CODE: ', code

  def result(self):
    self.dump_stacks()
    print '---'*10
    while self.execute():
      #self.dump_stacks()
      pass
    print '---'*10
    self.dump_stacks()



if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

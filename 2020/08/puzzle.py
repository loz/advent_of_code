import copy

class Puzzle:

  def process(self, text):
    self.instructions = []
    self.accumulator = 0
    lines = text.split('\n')
    for line in lines:
      if line.strip() != '':
        self.instructions.append(self.parse_line(line))
    self.instruction_pointer = 0
  
  def parse_line(self, line):
    op, val = line.split(' ')
    return (op, int(val))

  def run_statement(self):
    instruction = self.instructions[self.instruction_pointer]
    print 'run> ', instruction
    op, val = instruction
    if op == 'nop':
      pass
    elif op == 'acc':
      self.accumulator = self.accumulator + val
    elif op == 'jmp':
      self.instruction_pointer = self.instruction_pointer + val - 1
    self.instruction_pointer = self.instruction_pointer + 1

  def terminated(self):
    return self.instruction_pointer == len(self.instructions)

  def result(self):
    visited = {}
    while not visited.has_key(self.instruction_pointer):
      visited[self.instruction_pointer] = True
      self.run_statement()
    print 'Repeats: ', self.instruction_pointer, self.accumulator

  def result2(self):
    print 'here'
    original = copy.copy(self.instructions)
    for i in range(0, len(original)):
      attempt = copy.copy(original)
      inst = attempt[i]
      op, val = inst
      if op == 'nop':
        print 'swapping nop @', i
        attempt[i] = ('jmp', val)
      elif op == 'jmp':
        print 'swapping jmp @', i
        attempt[i] = ('nop', val)
      else:
        next
      self.instruction_pointer = 0
      self.accumulator = 0
      self.instructions = attempt
      visited = {}
      while not self.terminated() and not visited.has_key(self.instruction_pointer):
        visited[self.instruction_pointer] = True
        self.run_statement()
      if self.terminated():
        print 'Fixed!', i, self.accumulator
        exit()
      else:
        print 'Repeats: ', i, self.instruction_pointer, self.accumulator

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result2()

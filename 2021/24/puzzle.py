class Puzzle:
  def __init__(self):
    self.instructions = []
    self.reg = {
      'w': 0,
      'x': 0,
      'y': 0,
      'z': 0
    }

  def process(self, text):
    for line in text.split('\n'):
      if len(line) > 0:
        self.process_line(line)

  def process_line(self, line):
    parts = line.split(' ')
    op = parts[0]
    rands = parts[1:]
    self.instructions.append((op, rands))

  def run(self, input):
    input = [int(ch) for ch in input]
    for i in self.instructions:
      input = self.execute(i, input)

  def execute(self, instruction, input):
    op, rands = instruction
    if op == 'inp':
      dest = rands[0]
      self.reg[dest] = input[0]
      input = input[1:]
    elif op == 'add':
      dest = rands[0]
      val1 = self.reg[dest]
      val2 = self.get_val(rands[1])
      self.reg[dest] = val1 + val2
    elif op == 'mul':
      dest = rands[0]
      val1 = self.reg[dest]
      val2 = self.get_val(rands[1])
      self.reg[dest] = val1 * val2
    elif op == 'div':
      dest = rands[0]
      val1 = self.reg[dest]
      val2 = self.get_val(rands[1])
      self.reg[dest] = val1 / val2
    elif op == 'mod':
      dest = rands[0]
      val1 = self.reg[dest]
      val2 = self.get_val(rands[1])
      self.reg[dest] = val1 % val2
    elif op == 'eql':
      dest = rands[0]
      val1 = self.reg[dest]
      val2 = self.get_val(rands[1])
      if (val1 == val2):
        res = 1
      else:
        res = 0
      self.reg[dest] = res
    return input

  def get_val(self, loc):
    try:
      val = int(loc)
      return val
    except:
      return self.reg[loc]

  def result(self):
    pass

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

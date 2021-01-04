import re

class Puzzle:

  def process(self, text):
    self.reg = {}
    self.maxv = 0
    self.instructions = []
    lines = text.split('\n')
    for line in lines:
      if line.strip() != '':
        self.process_line(line)

  def process_line(self, line):
    pattern = re.compile(r"(\w+) (inc|dec) (-{0,1}\d+) if (\w+) (\>|\<|>=|<=|==|!=) (-{0,1}\d+)")
    match = pattern.match(line)
    groups = match.groups()
    self.instructions.append(((groups[0], groups[1], groups[2]), (groups[3], groups[4], groups[5])))

  def get_reg(self, name):
    return self.reg.get(name, 0)

  def set_reg(self, name, val):
    if val > self.maxv:
      self.maxv = val
    self.reg[name] = val

  def eval_cond(self, condition):
    or1, op, or2 = condition
    or1 = self.get_reg(or1)
    or2 = int(or2)
    if op == '==':
      return or1 == or2
    elif op == '<':
      return or1 < or2
    elif op == '>':
      return or1 > or2
    elif op == '<=':
      return or1 <= or2
    elif op == '>=':
      return or1 >= or2
    elif op == '!=':
      return or1 != or2
    else:
      raise 'Unknown', op

  def exec_action(self, action):
    or1, op, or2 = action
    val = self.get_reg(or1)
    if op == 'inc':
      val += int(or2)
      self.set_reg(or1, val)
    elif op == 'dec':
      val -= int(or2)
      self.set_reg(or1, val)

  def run(self):
    for instruction in self.instructions:
      action, condition = instruction
      if self.eval_cond(condition):
        self.exec_action(action)

  def result(self):
    self.run()
    print 'Registers:'
    print self.reg
    print 'Max Value Ever', self.maxv

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

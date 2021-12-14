class Puzzle:

  class Computer:
    def __init__(self, puzzle):
      self.ip = 0
      self.blocked = False

      self.reg = {
      }
      self.sends = []
      self.total_sent = 0
      self.recieved = []
      self.instructions = puzzle.instructions

    def read_val(self, val):
      try:
        return int(val)
      except:
        return self.reg.get(val, 0)

    def run(self, inputbuffer = []):
      while self.ip < len(self.instructions):
        current = self.instructions[self.ip]
        #print current
        op = current[0]
        if op == 'snd':
          val = self.read_val(current[1])
          self.total_sent += 1
          self.sends.append(val)
        elif op == 'set':
          dst = current[1]
          val = self.read_val(current[2])
          self.reg[dst] = val
        elif op == 'add':
          dst = current[1]
          val = self.read_val(current[2])
          self.reg[dst] = self.reg.get(dst, 0) + val
        elif op == 'mul':
          dst = current[1]
          val = self.read_val(current[2])
          self.reg[dst] = self.reg.get(dst, 0) * val
        elif op == 'mod':
          dst = current[1]
          val = self.read_val(current[2])
          self.reg[dst] = self.reg.get(dst, 0) % val
        elif op == 'rcv':
          dst = current[1]
          if len(inputbuffer) > 0:
            val = inputbuffer[0]
            inputbuffer = inputbuffer[1:]
            self.reg[dst] = val
            self.recieved.append(val)
          else:
            self.blocked = True
            return
        elif op == 'jgz':
          val = self.read_val(current[1])
          off = self.read_val(current[2])
          #print 'Jump', val, off
          if val > 0:
            self.ip += (off - 1)
        self.ip += 1

  def process(self, text):
    self.instructions = []

    lines = text.split('\n')
    for line in lines:
      self.process_line(line)


  def process_line(self, line):
    if len(line) > 0:
      parts = line.split(' ')
      self.instructions.append(parts)


  def result(self):
    comp1 = Puzzle.Computer(self)
    comp2 = Puzzle.Computer(self)
    comp1.id = 0
    comp2.id = 1
    comp1.reg['p'] = 0
    comp2.reg['p'] = 1
    computers = [comp1, comp2]
    active = 1
    print 'Run', comp1.id, []
    comp1.run([])
    print '=>', comp1.sends
    while len(comp1.sends) + len(comp2.sends) > 0:
      other = 1 - active
      comp_a = computers[active]
      comp_b = computers[other]
      print 'Run', comp_a.id, comp_b.sends
      comp_a.run(comp_b.sends)
      print '=>', comp_a.sends
      comp_b.sends = []
      active = other
    print 'Comp', comp1.id, comp1.total_sent, comp1.reg
    print 'Comp', comp2.id, comp2.total_sent, comp2.reg

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

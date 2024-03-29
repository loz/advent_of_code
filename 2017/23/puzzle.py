import sys

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
        elif op == 'sub':
          dst = current[1]
          val = self.read_val(current[2])
          self.reg[dst] = self.reg.get(dst, 0) - val
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
        elif op == 'jnz':
          val = self.read_val(current[1])
          off = self.read_val(current[2])
          #print 'Jump', val, off
          if val != 0:
            self.ip += (off - 1)
        else:
          print 'Operation Not Implemented:' + op
        self.ip += 1
        print self.ip, self.reg

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
    computer = Puzzle.Computer(self)
    computer.reg['a'] = 10
    computer.reg['h'] = 0
    computer.run([])

if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

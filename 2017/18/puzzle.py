class Puzzle:

  def process(self, text):
    self.instructions = []
    self.ip = 0

    self.reg = {
    }
    self.sounds = []
    self.recovered = []

    lines = text.split('\n')
    for line in lines:
      self.process_line(line)

  def process_line(self, line):
    if len(line) > 0:
      parts = line.split(' ')
      self.instructions.append(parts)

  def run(self):
    while self.ip < len(self.instructions):
      current = self.instructions[self.ip]
      #print current
      op = current[0]
      if op == 'snd':
        val = self.read_val(current[1])
        self.sounds.append(val)
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
        val = self.read_val(current[1])
        if val != 0:
          self.recovered.append(self.sounds[len(self.sounds)-1])
          return
      elif op == 'jgz':
        val = self.read_val(current[1])
        off = self.read_val(current[2])
        #print 'Jump', val, off
        if val > 0:
          self.ip += (off - 1)
      self.ip += 1

  def read_val(self, val):
    try:
      return int(val)
    except:
      return self.reg.get(val, 0)

  def result(self):
    self.run()
    print self.sounds
    print self.recovered

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

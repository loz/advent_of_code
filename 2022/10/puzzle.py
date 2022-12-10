import sys

class Puzzle:

  def process(self, text):
    self.x = 1
    self.instructions = []
    self.instptr = 0
    self.clockcycle = 0
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      if line == 'noop':
        op, opand = 'noop', None
      else:
        op, opand = line.split(' ')
      self.instructions.append((op, opand))

  def execute(self):
    op, opand = self.instructions[self.instptr]
    if op == 'addx':
      if self.clockcycle == 0:
        self.clockcycle = 1
        return
      else:
        self.clockcycle = 0
        val = int(opand)
        self.x += val
    self.instptr += 1
    if self.instptr == len(self.instructions):
      self.instptr = 0

  def result1(self):
    strength = 0
    count = 20
    for i in range(20-1):
      self.execute()
    val = count * self.x
    strength += val
    print count, '=>', self.x, '=>', val
    self.execute()

    for l in range(5):
      count += 40
      for i in range(40-1):
        self.execute()
      val = count * self.x
      strength += val
      print count, '=>', self.x, '=>', val
      self.execute()

    print 'Strength', strength

  def result(self):
    for y in range(6):
      for x in range(40):
        lit = False
        if x in range(self.x-1, self.x+2):
          lit = True
        if lit:
          sys.stdout.write('#')
        else:
          sys.stdout.write('.')
        self.execute()
      print


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

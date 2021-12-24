class Puzzle:
  def __init__(self):
    self.instructions = []

  def process(self, text):
    for line in text.split('\n'):
      if len(line) > 0:
        self.process_line(line)

  def process_line(self, line):
    parts = line.split(' ')
    op = parts[0]
    rands = parts[1:]
    self.instructions.append((op, rands))

  def runfast(self, input):
    w = input[0]
    x=1
    y=w+12
    z=y

    w = input[1]
    z=z*26
    y=w+6
    z=z+y

    w = input[2]
    z=z*26
    y=w+4
    z=z+y

    w = input[3]
    z=z*26
    y=w+5
    z=z+y

    w = input[4]
    z=z*26
    y=w
    z=z+y

    #Now it matters on the mod
    w = input[5]
    x = z % 26
    z = z / 26
    x -= 7
    if x == input: #Calc matches DIG 5
      x = 0
      y = 1
    else:
      x = 1
      y = 26
    z=z*y
    z=z+w+4


    pass

  def genkey(self, fivenum, twonum):
    digits = []
    #DIG-0-4
    w = fivenum[0]
    sha = w + 12
    w = fivenum[1]
    sha *= 26
    sha = sha + w + 6
    w = fivenum[2]
    sha *= 26
    sha = sha + w + 4
    w = fivenum[3]
    sha *= 26
    sha = sha + w + 5
    w = fivenum[4]
    sha *= 26
    sha = sha + w

    #DIG-5
    chk = (sha % 26) - 7
    sha = sha / 26
    digits.append(chk)

    #DIG-6
    chk = (sha % 26) - 13
    sha = sha / 26
    digits.append(chk)

    #DIG-7 from other two
    w = twonum[0]
    digits.append(w)
    sha *= 26
    sha = sha + w + 14

    #DIG-8
    chk = (sha % 26) - 7
    sha = sha / 26
    digits.append(chk)

    #DIG-9 Any other two, 2nd
    w = twonum[1]
    digits.append(w)
    sha *= 26
    sha = sha + w + 14

    #DIG-10
    chk = (sha % 26) - 9
    sha = sha / 26
    digits.append(chk)

    #DIG-11
    chk = (sha % 26) - 2
    sha = sha / 26
    digits.append(chk)

    #DIG-12
    chk = (sha % 26) - 9
    sha = sha / 26
    digits.append(chk)

    #DIG-13
    chk = (sha % 26) - 14
    sha = sha / 26
    digits.append(chk)

    return fivenum + digits

  def run(self, input):
    self.reg = {
      'w': 0,
      'x': 0,
      'y': 0,
      'z': 0
    }
    self.stopped = False
    input = [int(ch) for ch in input]
    for i in self.instructions:
      input = self.execute(i, input)
      if self.stopped:
        return

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
    elif op == 'deb':
      print self.reg, ' '.join(rands)
    elif op == 'stp':
      self.stopped = True
    return input

  def get_val(self, loc):
    try:
      val = int(loc)
      return val
    except:
      return self.reg[loc]

  def decrement(self, num):
    num -= 1
    while '0' in str(num):
      num -=1
    return num

  def increment(self, num):
    num += 1
    while '0' in str(num):
      num +=1
    return num

  def result1(self):
    num = 11111
    #for _ in range(1000):
    while num <= 99999:
      test = [int(ch) for ch in str(num)]
      num2 = 11
      while num2 <= 99:
        test2 = [int(ch) for ch in str(num2)]
        key = self.genkey(test, test2)
        invalid = filter(lambda n: n<1 or n>9, key)
        if len(invalid) > 0:
          #print key, 'INVALID'
          pass
        else:
          print key, 'VALID'
          txt = map(lambda n: str(n), key)
          print ''.join(txt)
          return
        num2 = self.increment(num2)
      num = self.increment(num)
    return

  def result(self):
    num = 94748111816194
    num = 94748111816199
    #num = 99999231816299
    num = 99799212949967
    test = str(num)
    self.run(test)
    print 'Run', test, ':', self.reg

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result1()

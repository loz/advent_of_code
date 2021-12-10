class Puzzle:

  def process(self, text):
    pass

  def result1(self):
    total = 0
    #a = 65 
    #b = 8921
    a = 116
    b = 299
    for n in range(40000000):
      a = self.generateA(a)
      b = self.generateB(b)
      if self.judge(a, b):
        total += 1
    print 'Total:', total

  def result(self):
    total = 0
    #a = 65 
    #b = 8921
    a = 116
    b = 299
    for n in range(5000000):
      a = self.generateA2(a)
      b = self.generateB2(b)
      if self.judge(a, b):
        total += 1
    print 'Total:', total

  def generateA(self, seed):
    return (seed * 16807) % 2147483647

  def generateA2(self, seed):
    seed = (seed * 16807) % 2147483647
    while seed & 0b0011 != 0:
      seed = (seed * 16807) % 2147483647
    return seed

  def generateB(self, seed):
    return (seed * 48271) % 2147483647

  def generateB2(self, seed):
    seed = (seed * 48271) % 2147483647
    while seed & 0b0111 != 0:
      seed = (seed * 48271) % 2147483647
    return seed

  def judge(self, a, b):
    return 0b00000000000000001111111111111111 & a == 0b00000000000000001111111111111111 & b

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

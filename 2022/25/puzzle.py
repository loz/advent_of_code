import sys

class Puzzle:

  def process(self, text):
    self.numbers = []
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      self.numbers.append(line)
  
  def eval(self, text):
    n = 0
    for ch in text:
      n *= 5
      if ch == '1':
        n += 1
      elif ch == '0':
        n += 0
      elif ch == '2':
        n += 2
      elif ch == '-':
        n += -1
      elif ch == '=':
        n += -2
    return n

  def snafu(self, n):
    num = ""
    carry = 0
    while n+carry != 0:
      rem = n % 5
      rem += carry
      carry = 0
      if rem == 0:
        num = '0' + num
      elif rem == 1:
        num = '1' + num
      elif rem == 2:
        num = '2' + num
      elif rem == 3:
        num = '=' + num
        carry = 1
      elif rem == 4:
        num = '-' + num
        carry = 1
      elif rem == 5:
        num = '0' + num
        carry = 1
      n = n / 5
     # print 'Rem', rem, n, carry, num
    return num

  def result(self):
    total = 0
    for n in self.numbers:
      v = self.eval(n)
      print n, '=>', v
      total += v
    print 'Total', total
    sn = self.snafu(total)
    print 'ASSERT:', total == self.eval(sn)
    print 'Sanfu', sn
    #print 'Total:', self.eval(sn)



if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

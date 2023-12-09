import sys

class Puzzle:

  def process(self, text):
    self.readings = []
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      reading = [int(n) for n in line.split(' ')]
      self.readings.append(reading)

  def reduce(self, readings):
    nr = []
    for n in range(len(readings) - 1):
      #diff = abs(readings[n+1]-readings[n])
      diff = (readings[n+1]-readings[n])
      nr.append(diff)
    return nr

  def r_generate(self, readings):
    if all([r == 0 for r in readings]):
      #print('->', readings)
      return 0
    else:
      last = readings[len(readings)-1]
      n = self.r_generate(self.reduce(readings))
      #print('->', readings, '=>', last + n)
      return last + n

  def generate(self, readings):
    n = self.r_generate(readings)
    #print(readings, '=>', n)
    print(readings,n)
    return n

  def result(self):
    self.result2()

  def result2(self):
    #Reverse
    back = []
    for r in self.readings:
      rr = list(reversed(r))
      back.append(rr)

    total = 0
    for r in back:
      #print('Reading', r)
      n = self.generate(r)
      total += n
      #print(total)
      #print('=', n)
    print('Total', total)

  def result1(self):
    total = 0
    for r in self.readings:
      #print('Reading', r)
      n = self.generate(r)
      total += n
      #print(total)
      #print('=', n)
    print('Total', total)

if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

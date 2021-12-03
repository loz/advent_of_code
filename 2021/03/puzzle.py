class Puzzle:
  def __init__(self):
    self.gamma = 0
    self.epsilon = 0
    self.bit_counts = {}

  def process(self, text):
    lines = text.split('\n')
    for line in lines:
      self.process_line(line)
    self.compute_gamma()
    self.compute_epsilon()

  def compute_gamma(self):
    gamma = []
    numbits = len(self.bit_counts) / 2
    #print numbits
    #print len(self.bit_counts)
    #print self.bit_counts
    for bit in range(numbits):
      zero_count = self.bit_counts[(bit,'0')]
      one_count = self.bit_counts[(bit,'1')]
      if zero_count > one_count:
        gamma.append('0')
      else:
        gamma.append('1')
      
    self.gamma = int(''.join(gamma), 2)

  def compute_epsilon(self):
    epsilon = []
    numbits = len(self.bit_counts) / 2
    #print numbits
    #print len(self.bit_counts)
    #print self.bit_counts
    for bit in range(numbits):
      zero_count = self.bit_counts[(bit,'0')]
      one_count = self.bit_counts[(bit,'1')]
      if zero_count < one_count:
        epsilon.append('0')
      else:
        epsilon.append('1')
      
    self.epsilon = int(''.join(epsilon), 2)

  def process_line(self, line):
    pos = 0
    for bit in line:
      count = self.bit_counts.get((pos,bit), 0)
      count +=1
      self.bit_counts[(pos,bit)] = count
      pos += 1

  def result(self):
    print 'Gamma', self.gamma
    print 'Epsilon', self.epsilon
    print 'Result', self.gamma * self.epsilon

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

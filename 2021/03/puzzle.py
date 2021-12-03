class Puzzle:
  def __init__(self):
    self.gamma = 0
    self.epsilon = 0
    self.o2rating = 0
    self.co2rating = 0
    self.bit_counts = {}
    self.bitsets = []

  def process(self, text):
    lines = text.split('\n')
    for line in lines:
      self.process_line(line)
    gamma = self.compute_gamma(self.bitsets)
    self.gamma = int(''.join(gamma), 2)
    epsilon = self.compute_epsilon(self.bitsets)
    self.epsilon = int(''.join(epsilon), 2)
    self.compute_o2rating()
    self.compute_co2rating()


  def narrow(self, pos, bit, sets = None):
    if sets == None:
      sets = self.bitsets
    matching = []
    for bits in sets:
      if bits[pos] == bit:
        matching.append(bits)
    return matching

  def compute_o2rating(self):
    bitsets = self.bitsets
    bit = 0
    while len(bitsets) > 1:
      gamma = self.compute_gamma(bitsets)
      bitsets = self.narrow(bit, gamma[bit], bitsets)
      bit+=1
    self.o2rating = int(''.join(bitsets[0]), 2)

  def compute_co2rating(self):
    bitsets = self.bitsets
    bit = 0
    while len(bitsets) > 1:
      epsilon = self.compute_epsilon(bitsets)
      bitsets = self.narrow(bit, epsilon[bit], bitsets)
      bit+=1
    self.co2rating = int(''.join(bitsets[0]), 2)

  def compute_gamma(self, bitsets):
    gamma = []
    bit_counts = self.count_bits(bitsets)
    numbits = len(bitsets[0])
    for bit in range(numbits):
      zero_count = bit_counts.get((bit,'0'),0)
      one_count =  bit_counts.get((bit,'1'),0)
      if zero_count > one_count:
        gamma.append('0')
      else:
        gamma.append('1')
    return gamma

  def compute_epsilon(self, bitsets):
    epsilon = []
    bit_counts = self.count_bits(bitsets)
    numbits = len(bitsets[0])
    for bit in range(numbits):
      zero_count = bit_counts.get((bit,'0'),0)
      one_count =  bit_counts.get((bit,'1'),0)
      if zero_count <= one_count:
        epsilon.append('0')
      else:
        epsilon.append('1')
    return epsilon

  def count_bits(self, bitset):
    bit_counts = {}
    for bits in bitset:
      pos = 0
      for bit in bits:
        count = bit_counts.get((pos,bit), 0)
        count +=1
        bit_counts[(pos,bit)] = count
        pos += 1
    return bit_counts

  def process_line(self, line):
    if len(line) == 0:
      return
    bits = []
    for bit in line:
      bits.append(bit)
    self.bitsets.append(bits)

  def result(self):
    print 'Gamma', self.gamma
    print 'Epsilon', self.epsilon
    print 'Result', self.gamma * self.epsilon
    print 'O2 Rating', self.o2rating
    print 'CO2 Rating', self.co2rating
    print 'Result', self.o2rating * self.co2rating

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

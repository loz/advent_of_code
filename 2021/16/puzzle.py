class Puzzle:
  class Packet:
    def __init__(self):
      self.eof = False
      self.subpackets = []
    
    def eval(self):
      if self.id == 4: #literal
        return self.literal
      elif self.id == 0: #sum
        total = 0
        for p in self.subpackets:
          total += p.eval()
        return total
      elif self.id == 1: #product
        total = 1
        for p in self.subpackets:
          total *= p.eval()
        return total
      elif self.id == 2: #min
        vals = [p.eval() for p in self.subpackets]
        return min(vals)
      elif self.id == 3: #max
        vals = [p.eval() for p in self.subpackets]
        return max(vals)
      elif self.id == 5: #gt
        v1 = self.subpackets[0].eval()
        v2 = self.subpackets[1].eval()
        if v1 > v2:
          return 1
        else:
          return 0
      elif self.id == 6: #lt
        v1 = self.subpackets[0].eval()
        v2 = self.subpackets[1].eval()
        if v1 < v2:
          return 1
        else:
          return 0
      elif self.id == 7: #eq
        v1 = self.subpackets[0].eval()
        v2 = self.subpackets[1].eval()
        if v1 == v2:
          return 1
        else:
          return 0

    def pull(self, count, bitstream):
      data = bitstream[0:count]
      return data, bitstream[count:]
    
    def version_total(self):
      total = self.version
      for packet in self.subpackets:
        total += packet.version_total()
      return total

    def bitint(self, bits):
      bits = map(lambda b: str(b), bits)
      bits = ''.join(bits)
      return int(bits, 2)

    def pull_packet(self, bitstream):
      try:
        ver, bitstream = self.pull(3, bitstream)
        self.version = self.bitint(ver)
        pid, bitstream = self.pull(3, bitstream)
        self.id = self.bitint(pid)
        if self.id == 4:
          #Literal
          lbits = []
          bits, bitstream = self.pull(5, bitstream)
          while bits[0] == 1:
            bits = bits[1:]
            lbits += bits
            bits, bitstream = self.pull(5, bitstream)
          bits = bits[1:]
          lbits += bits
          self.literal = self.bitint(lbits)
        else: #operator
          ltype, bitstream = self.pull(1, bitstream)
          ltype = ltype[0]
          self.ltype = ltype
          if ltype == 0:
            lbits, bitstream = self.pull(15, bitstream)
            self.length = self.bitint(lbits)
            subbits, bitstream = self.pull(self.length, bitstream)
            while len(subbits) > 0:
              subpacket = Puzzle.Packet()
              subbits = subpacket.pull_packet(subbits)
              self.subpackets.append(subpacket)
          else:
            lbits, bitstream = self.pull(11, bitstream)
            self.length = self.bitint(lbits)
            for p in range(self.length):
              subpacket = Puzzle.Packet()
              bitstream = subpacket.pull_packet(bitstream)
              self.subpackets.append(subpacket)
        return bitstream
      except: #empty
        self.eof = True
        return []

  DECODE = {
    '0' : [0,0,0,0],
    '1' : [0,0,0,1],
    '2' : [0,0,1,0],
    '3' : [0,0,1,1],
    '4' : [0,1,0,0],
    '5' : [0,1,0,1],
    '6' : [0,1,1,0],
    '7' : [0,1,1,1],
    '8' : [1,0,0,0],
    '9' : [1,0,0,1],
    'A' : [1,0,1,0],
    'B' : [1,0,1,1],
    'C' : [1,1,0,0],
    'D' : [1,1,0,1],
    'E' : [1,1,1,0],
    'F' : [1,1,1,1]
  }

  def process(self, text):
    self.bitstream = []
    self.decode_bits(text)

  def get_packet(self):
    packet = Puzzle.Packet()
    self.bitstream = packet.pull_packet(self.bitstream)
    return packet

  def decode_bits(self, text):
    text=text.strip()
    for ch in text:
      bits = self.DECODE[ch]
      self.bitstream += bits

  def result1(self):
    version_total = 0
    while len(self.bitstream) > 0:
      packet = self.get_packet()
      if not packet.eof:
        version_total += packet.version_total()
    print 'Version Total', version_total

  def result(self):
    while len(self.bitstream) > 0:
      packet = self.get_packet()
      if not packet.eof:
        print 'Packet: ', packet.eval()

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

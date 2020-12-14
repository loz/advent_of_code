import copy

class Puzzle:

  def process(self, text):
    lines = text.split('\n')
    self.memory = {}
    for line in lines:
      if line.strip() != '':
        if line.startswith('mask'):
          mask = line.replace('mask = ', '')
          self.mask = []
          for ch in mask:
              self.mask.append(ch)
          #print 'Set Mask', self.mask
        else:
          mem, num = line.split(' = ')
          num = int(num)
          mem = mem.replace('mem[', '').replace(']', '')
          mem = int(mem)
          #print mem, '=', num
          addrs = self.apply_mask(mem)
          for addr in addrs:
            self.memory[addr] = num

  def _gen_variant(self, mask):
    #No variant
    xs = filter(lambda b: b == 'X', mask)
    if len(xs) == 0:
      bits = map(lambda b: str(b), mask)
      return [int(''.join(bits), 2)]
    variants = []
    for i in range(len(mask)):
      if mask[i] == 'X':
        v1 = copy.copy(mask)       
        v2 = copy.copy(mask)
        v1[i] = 0
        v2[i] = 1
        return self._gen_variant(v1) + self._gen_variant(v2)
    

  def apply_mask(self,num):
    bits = list("{0:b}".format(num))
    cmask = len(self.mask)
    cbits = len(bits)

    newbits = []
    while cmask > 0 or cbits > 0:
      bit = 0
      msk = 'X'
      if cmask > 0:
        cmask -= 1
        msk = self.mask[cmask]
      if cbits > 0:
        cbits -= 1
        bit = bits[cbits]
      if msk == '0':
        newbits.append(str(bit))
      elif msk == '1':
        newbits.append('1')
      else:
        newbits.append('X')
    #reverse
    newbits.reverse()
    #print 'Addr', bits, self.mask, '->', newbits
    #newbin = ''.join(newbits)
    return self._gen_variant(newbits)

  def result(self):
    total = 0 
    print '======= RESULT ======='
    for key in self.memory:
      value = self.memory[key]
      total += value
      print key, value
    print 'SUM', total

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

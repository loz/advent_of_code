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
          self.memory[mem] = self.apply_mask(num)

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
      if msk == 'X':
        newbits.append(str(bit))
      else:
        newbits.append(msk)
    #reverse
    newbits.reverse()
    newbin = ''.join(newbits)
    return int(newbin, 2)

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

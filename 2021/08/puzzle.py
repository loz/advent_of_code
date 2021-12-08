class Puzzle: 

  def process(self, text):
    self.outputs = []
    self.inputs = []
    self.bitmasks = {
     0: 0b1110111,
     1: 0b0010010,
     2: 0b1011101,
     3: 0b1011011,
     4: 0b0111010,
     5: 0b1101011,
     6: 0b1101111,
     7: 0b1010010,
     8: 0b1111111,
     9: 0b1111011
    }

    lines = text.split('\n')
    for line in lines:
      self.process_line(line)
        
  def toset(self, pattern):
    return set([ch for ch in pattern])

  def toskey(self, key):
    skey = list(key)
    skey.sort()
    return ''.join(skey)
    

  def genmasks(self, patterns):
    masks = {}
    known = []
    unknown = map(lambda p: self.toset(p), patterns.split(' '))
    for pattern in patterns.split(' '):
      opts = self.map_options(pattern)
      key =  self.toset(pattern)
      skey = self.toskey(key)
      if len(opts) == 1:
        known.append(key)
        unknown.remove(key)
        masks[skey] = opts[0]
      else:
        masks[skey] = opts
    print known, unknown
    if len(unknown) > 0:
      print 'More to Sort', masks
      for item in unknown:
        skey = self.toskey(item)
        for kitem in known:
          if kitem.issubset(item):
            print 'Known In Unknown', kitem
            kmask = masks[self.toskey(kitem)]
            umask = masks[skey]
            print self.bin_strs([kmask]), 'v', self.bin_strs(umask)
            matches = []
            for m in umask:
              if (kmask & m) == kmask:
                matches.append(m)
            if len(matches) == 1:
              unknown.remove(item)
              masks[skey] = matches[0]
              break
            else:
              masks[skey] = matches
    return masks

  def bin_strs(self, arr):
    return '[' + ','.join(map(lambda b: "{:08b}".format(b), arr)) + ']'

  def process_line(self, line):
    if len(line) > 0:
      patterns, digits = line.split(' | ')
      self.inputs.append((patterns, digits))
      numbers = self.map_digits(digits)
      self.outputs.append(numbers)

  def map_options(self, signal):
    l = len(signal)
    if l == 2:
      return [self.bitmasks[1]]
    elif l == 3:
      return [self.bitmasks[7]]
    elif l == 4:
      return [self.bitmasks[4]]
    elif l == 5:
      return [self.bitmasks[2], self.bitmasks[3], self.bitmasks[5]]
    elif l == 6:
      return [self.bitmasks[0], self.bitmasks[6], self.bitmasks[9]]
    elif l == 7:
      return [self.bitmasks[8]]

  def map_digits(self, digits):
    digits = digits.split(' ')
    mapped = []
    for digit in digits:
      l = len(digit)
      if l == 2:
        mapped.append(1)
      elif l == 3:
        mapped.append(7)
      elif l == 4:
        mapped.append(4)
      elif l == 7:
        mapped.append(8)
    return mapped

  def result1(self):
    total = 0
    for output in self.outputs:
      print output
      total += len(output)
    print 'Total 1, 4, 7, 8s:', total

  def result(self):
    for i in self.inputs:
      print i
    i = self.inputs[0]
    pattern, digits = i
    options = self.narrow_options(pattern)
    for k in options:
      print k, options[k]
    options = self.narrow_options(pattern, options)
    for k in options:
      print k, options[k]


if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

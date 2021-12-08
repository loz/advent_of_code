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
    #find 1, 4, 7, 8
    unknown = self.map_sets(patterns)
    known, unknown = self.find_1478(unknown)
    known, unknown = self.find_906(known, unknown)
    known = self.find_352(known, unknown)
    return known

  def find_1478(self, unknown):
    known = {}
    new_unknown = []
    for item in unknown:
      l = len(item)
      if l == 2:
        known[1] = item
      elif l == 3:
        known[7] = item
      elif l == 4:
        known[4] = item
      elif l == 7:
        known[8] = item
      else:
        new_unknown.append(item)
    return known, new_unknown

  def find_906(self, known, unknown):
    new_unknown = []
    for item in unknown:
      if len(item) == 6:
        #possible 9, 0, 6
        if known[4].issubset(item):
          known[9] = item
        elif known[7].issubset(item):
          known[0] = item
        else:
          known[6] = item
      else:
        new_unknown.append(item)

    return known, new_unknown

  def find_352(self, known, unknown):
    new_unknown = []
    for item in unknown:
      if known[7].issubset(item):
        known[3] = item
      elif item.issubset(known[9]):
        known[5] = item
      else:
        known[2] = item

    return known

  def map_sets(self, patterns):
    sets = patterns.split(' ')
    return map(lambda s: self.toset(s), sets)

  def genmasks1(self, patterns):
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
    total = 0
    for i in self.inputs:
      patterns, code = i
      masks = self.genmasks(patterns)
      dcode = self.decode(code, masks)
      total += dcode
      print patterns, code, dcode
    print 'Total', total

  def decode(self, code, masks):
    setcode = self.map_sets(code)
    dcode = 0
    for digit in setcode:
      for n in range(10):
        if masks[n] == digit:
          dcode *= 10
          dcode += n
    return dcode


if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

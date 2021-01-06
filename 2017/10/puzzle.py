class Puzzle:

  def process(self, text):
    lengths = text.split(',')
    self.lengths = map(lambda x: int(x), lengths)
    self.cursor = 0
    self.skip = 0

  def knot(self):
    length = self.lengths.pop(0)
    if length > len(self.items):
      length = len(self.items)
    start = self.cursor
    end = start + length
    #print 'Knot', length, len(self.items)
    before = self.items[0:start]
    cut = self.items[start:end]
    after = self.items[end:]
    if end > len(self.items):
      offset = end - len(self.items)
      lencut = len(cut)
      cut += before[0:offset]
      before = before[offset:]
      #print before, cut, after
      cut.reverse()
      before = cut[lencut:] + before
      cut = cut[0:lencut]
      #print '>>', before, cut, after
    else:
      #print before, cut, after
      cut.reverse()
      self.items = before + cut + after
    self.items = before + cut + after
    self.cursor += length + self.skip
    self.skip += 1
    self.cursor = self.cursor % len(self.items)

  def encode(self):
    while len(self.lengths):
      self.knot()

  def hash(self, string):
    lengths = map(lambda x: ord(x), [ch for ch in string])
    lengths = lengths + [17, 31, 73, 47, 23]
    self.items = list(range(256))
    self.cursor = 0
    self.skip = 0
    for i in range(64):
      self.lengths = map(lambda x: x, lengths)
      self.encode()
    dense = self.calc_dense(self.items)
    dense = map(lambda x: "%0.2x" % x, dense)
    return ''.join(dense)

  def xor_chunk(self, chunk):
    value = chunk.pop(0)
    for num in chunk:
      value = value ^ num
    return value
    
  def calc_dense(self, items):
    #print 'Calc Dense'
    start = 0
    chunks = []
    while start < len(items):
      chunk = items[start:start+16]
      num = self.xor_chunk(chunk)
      start+=16
      chunks.append(num)
    return chunks

  def result(self):
    self.items = list(range(256))
    self.encode()
    print 'First', self.items[0]
    print 'Second', self.items[1]
    print 'Mult', self.items[0] * self.items[1]

  def result2(self, input):
    input = input.strip()
    print 'Hash', self.hash(input)

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()
  puz.result2(inp)

import sys

class Puzzle:

  def process(self, text):
    self.packets = []
    text = text.rstrip('\n')
    for pair in text.split('\n\n'):
      self.process_pair(pair)

  def process_pair(self, pair):
    left, right = pair.split('\n')
    left = self.process_packet(left)
    right = self.process_packet(right)
    self.packets.append((left, right))

  def process_packet(self, packet):
    tokens = [ch for ch in packet]
    v, _ = self.parse_tokens(tokens)
    return v[0]

  def parse_tokens(self, tokens):
    hasval = False
    val = 0
    arr = []
    while tokens:
      token = tokens.pop(0)
      if token == '[':
        hasval = False
        v, tokens = self.parse_tokens(tokens)
        arr.append(v)
      elif token == ']':
        if hasval:
          arr.append(val)
        return arr, tokens
      elif token == ',':
        if hasval:
          arr.append(val)
        val = 0
      elif token == ' ':
        pass
      else:
        hasval = True
        v = int(token)
        val = (10*val) + v
    return arr, []

  def _cmp(self, a, b, nest):
    if isinstance(a, list) and not isinstance(b, list):
      b = [b]
    elif not isinstance(a, list) and isinstance(b, list):
      a = [a]

    if isinstance(a, list):
      return self.cmp(a, b, nest + '  ')

    #print nest + '- Compare', a, 'vs', b

    if a < b:
      return -1
    elif a > b:
      return 1
    else:
      return 0

  def cmp(self, a, b, nest = ''):
    #print nest + '- Compare', a, 'vs', b
    l = min(len(a), len(b))
    for i in range(l):
      va = a[i]
      vb = b[i]
      c = self._cmp(va, vb, nest)
      if c != 0:
        return c
    #Assert all match
    if len(b) < len(a):
      return 1
    elif len(b) == len(a):
      return 0
    return -1


  def result1(self):
    total = 0
    for idx in range(len(self.packets)):
      p1, p2 = self.packets[idx]
      if self.cmp(p1, p2) == -1:
        print 'Packet', idx+1, 'out of order'
        total += idx+1
    print 'Sum', total
        
  def result(self):
    allpackets = []
    for pair in self.packets:
      p1, p2 = pair
      allpackets.append(p1)
      allpackets.append(p2)

    #add Divider packets
    allpackets.append([2])
    allpackets.append([6])

    allpackets.sort(cmp=self.cmp)
    for packet in allpackets:
      print packet
    
    p1 = allpackets.index([2]) + 1
    p2 = allpackets.index([6]) + 1
    print 'Indexes', p1, p2, '=>', p1 * p2



if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

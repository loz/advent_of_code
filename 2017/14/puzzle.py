class Puzzle:

  def process(self, text):
    self.code = text.rstrip()

  def result(self):
    print self.code
    total=0
    rows = []
    for row in range(128):
      rowcode = self.code + '-' + str(row)
      frag = self.frag_string(self.hash(rowcode))
      rows.append(frag)
      total += frag.count('#')
    regions = self.count_regions(rows)
    for row in rows:
      print row
    print 'Total:', total
    print 'Regions:', regions

  def frag_string(self, sha):
    frag = ""
    for ch in sha:
      hval = int(ch, 16)
      part = "{:04b}".format(hval)
      part = part.replace('0','.')
      part = part.replace('1','#')
      #print ch, hval, bin(hval), "{:04b}".format(hval)
      frag += part
    #print frag
    return frag

  def count_regions(self, rows):
    rmap = map(lambda r: [ch for ch in r], rows)
    count = 0
    h = len(rmap)
    w = len(rmap[0])
    for y in range(h):
      for x in range(w):
        if rmap[y][x] == '#':
          self.tag_region(rmap, x, y, w, h)
          count += 1
    return count

  def tag_region(self, rmap, x, y, w, h):
    toexplore = [(x,y)]
    explored = []
    while len(toexplore) > 0:
      pos = toexplore.pop()
      px, py = pos
      rmap[py][px] = 'R'
      explored.append(pos)
      neighbours = self.neighbours(px, py, w, h)
      for n in neighbours:
        nx, ny = n
        if rmap[ny][nx] == '#':
          toexplore.append(n)

  def neighbours(self, x, y, w, h):
    deltas = [(-1,0), (1,0), (0, -1), (0, 1)]
    neighbours = []
    for d in deltas:
      dx, dy = d
      xx = x + dx
      yy = y + dy
      if xx >=0 and xx < w and yy >= 0 and yy < h:
        neighbours.append((xx,yy))
    return neighbours
    
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

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

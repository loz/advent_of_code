class Puzzle:

  def __init__(self, size):
    self.size = size
    self.ranges = {0:size}
    self.blocks = []

  def valid(self, num):
    for block in self.blocks:
      start, finish = block
      if num >= start and num <= finish:
        return False
    return True

  def process(self, text):
    lines = text.split('\n')
    for line in lines:
      if line.strip() != '':
        self.block_range(line)
    self.optimize()

  def optimize(self):
    #print 'Optimise'
    self.blocks.sort(key=lambda b: b[0])
    newblocks = []
    current = self.blocks.pop(0)
    for block in self.blocks:
      #print current, 'vs', block
      #(0, 97802) vs (5682, 591077)
      if current[1] >= block[0]-1:
        if current[1] > block[1]:
          #print 'skip'
          pass
        else:
          current=(current[0], block[1])
      else:
        newblocks.append(current)
        current = block
    newblocks.append(current)
    self.blocks = newblocks
    #print '========='
    #for block in newblocks:
    #  print block


  def block_range(self, line):
    start, finish = map(lambda i: int(i), line.split('-'))
    self.blocks.append((start, finish))
    
  def block_range_old(self, line):
    start, finish = map(lambda i: int(i), line.split('-'))
    print start, '...', finish
    inany = False
    for ostart in self.ranges:
      oend = self.ranges[ostart]
      #print 'in', ostart, oend, '?'
      if start >= ostart and start <= oend:
        print 'start yes'
        if finish >= ostart and finish <= oend:
          print 'end yes'
          #split this range
          self.ranges[ostart] = start-1
          self.ranges[finish+1] = oend
          inany = True
          break
        else:
          print 'end, no'
          self.ranges[ostart] = start-1
          inany = True
          #break
      elif finish >= ostart and finish <= oend:
        print 'start no, end yes', ostart, oend
        self.ranges[ostart] = finish+1
        self.ranges[finish+1] = self.ranges[ostart]
        self.ranges.pop(ostart)
        inany = True
        #break
    if not inany:
      print 'in none', self.ranges
      raise 'boo'

  def result1(self):
    minv = 0
    while not self.valid(minv):
      minv +=1
    print 'Smallest', minv

  def result(self):
    avail = 0
    first = self.blocks.pop(0)
    print first
    lastend= first[1]
    for block in self.blocks:
      start, finish = block
      size = (start-lastend-1)
      avail += size
      print 'Free', lastend, '->', start, size, avail
      lastend = finish
    rest = 4294967295 - lastend
    print 'Rest', rest
    print 'Available', avail


if __name__ == '__main__':
  puz = Puzzle(4294967295)
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

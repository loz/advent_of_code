class Puzzle:

  def process(self, string):
    print 'Load', string
    ints = []
    for ch in string:
      ints.append(int(ch))
    self.dim = len(ints)
    self.head = ints[0]
    self.links = {}
    for i in range(self.dim):
      nx = i+1
      if nx == self.dim:
        nx = 0
      #print i, ints[i], '->', ints[nx]
      self.links[ints[i]] = ints[nx]
    print self.links, self.dim

  def fillfrom(self, loc, upper):
    origend = self.links[loc]
    start = self.dim+1
    endd = upper+1
    head = loc
    for i in range(start, endd):
      self.links[head] = i
      head = i
    self.links[i] = origend
    print 'Looping back', i, '->', origend
    self.dim = upper

  def trace(self, count, ffrom = None):
    if ffrom == None:
      ffrom = self.head
    values = []
    head = ffrom
    for i in range(count):
      values.append(head)
      head = self.links[head]
    return values

  def play(self):
    current = self.head # links -> after set
    first = self.links[current]  #insert link -> first
    second = self.links[first]
    third = self.links[second]
    newhead = self.links[third]  #link to -> insertend
    pick = [first, second, third]
    #print current, first, second, third, 'newhead', newhead
    insert = current - 1
    if insert == 0:
      insert = self.dim
    while insert in pick:
      insert -= 1
      if insert == 0:
        insert = self.dim
    insertend = self.links[insert]
    self.links[insert] = first
    self.links[self.head] = self.links[third]
    self.links[third] = insertend
    self.head = newhead

  def result(self, rounds):
    for i in range(rounds):
      #print 'move', i+1
      #print self.trace(9)
      self.play()
      #print puz.trace(101)
    print 'Final', 
    #print self.trace(9)
    #idx = cups.index(1)
    #print '1@', idx
    #print cups[idx+1]
    #print cups[idx+2]
    after = self.trace(9, 1)
    #after = map(lambda a: str(a), after)
    #print 'Labels', ''.join(after)
    print after[0]
    print after[1]
    print after[2]
    print after[1] * after[2]

if __name__ == '__main__':
  puz = Puzzle()
  #puz.result(1000)
  puz.process("942387615")
  puz.fillfrom(5, 1000000)
  #puz.process("389125467")
  #puz.fillfrom(7, 1000000)
  #puz.fillfrom(7, 100)
  print 'Filled'
  #puz.result(1000000)
  #puz.result(100)
  print puz.trace(101)
  #exit()
  #puz.result(10000000)
  puz.result(10000000+1)

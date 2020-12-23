class Puzzle:

  def process(self, text):
    pass
  
  def play(self, cups):
    dim = len(cups)
    pick = cups[1:4]
    dest = cups[0] - 1
    if dest == 0:
      dest = dim
    #print 'cups', cups
    #print 'pick', pick
    #print 'dest', dest
    newcups = cups[4:] + [cups[0]]
    while dest not in newcups:
      dest -= 1
      if dest == 0:
        dest = dim
    idx = newcups.index(dest)
    newcups = newcups[0:idx+1] + pick + newcups[idx+1:]
    return newcups

  def result(self, rounds):
    #cups = [3, 8, 9, 1, 2, 5, 4, 6, 7]
    cups = [9, 4, 2, 3, 8, 7, 6, 1, 5] + list(range(10,1000000))
    subs = rounds / 100
    for s in range(100):
      print '.'
      for i in range(subs):
        #print 'move', i+1
        #print cups
        cups = self.play(cups)
    #print 'Final', cups
    idx = cups.index(1)
    print '1@', idx
    print cups[idx+1]
    print cups[idx+2]
    #after = cups[idx+1:] + cups[0:idx]
    #after = map(lambda a: str(a), after)
    #print 'Labels', ''.join(after)

if __name__ == '__main__':
  puz = Puzzle()
  #puz.result(1000)
  puz.result(1000000)

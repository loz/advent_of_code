class Puzzle:

  def process(self, text):
    pass

  def expand_pop(self, exp, n):
    head, runend, rtype = exp
    rest = []
    if rtype == 'one':  #repeat n, n+1, n+2...
      popped = []
      for i in range(n):
        popped.append(head)
        head += 1
      rest = [(head, runend, 'one')]
      return (popped, rest)
    elif rtype == 'two': #repeat n, n+1, n+3, n+5...
      rest = []
      popped = []
      for i in range(n):
        if len(rest) == 0:
          rest = [head, head+1]
          head += 3
        n = rest.pop(0)
        popped.append(n)
      print popped, rest, head, runend
      return (popped, rest + [(head, runend, 'two')])
      raise 'WIP'
    else:
      raise 'Expand Pop Unhandled:' + rtype
    

  def expand_pick(self, pick, rest):
    if type(pick[0]) != type(1):  #first expands
      print 'Expand 1'
      exp = pick.pop(0)
      prest = pick
      pick, exp = self.expand_pop(exp, 3)
      #print pick, exp, prest, rest
      return (pick, exp + prest + rest)
    elif type(pick[1]) != type(1): #second expands
      print 'Expand 2'
    elif type(pick[2]) != type(1): #third expand
      print 'Expand 3'
    else: #no expand
      return (pick, rest)

  def play(self, cups, dim, theround):
    pick = cups[1:4]
    head = cups[0]
    if type(head) == type(1):
      dest = head - 1
      if dest == 0:
        dest = dim
      #print 'cups', cups
      #print 'pick', pick
      #print 'dest', dest
      rest = cups[4:]
      pick, rest = self.expand_pick(pick, rest)
      newcups = rest + [head]
      while dest not in newcups:
        dest -= 1
        if dest == 0:
          dest = dim
      idx = newcups.index(dest)
      newcups = newcups[0:idx+1] + pick + newcups[idx+1:]
      theround += 1
    else:
      #Special ranger
      print 'SPECIAL - EXPAND!', 
      head, runend, rtype = head
      if rtype == 'one': #repeat n, n+1, n+2...
        repeat = (runend - head) / 4
        print 'consume', repeat, 'times'
        print 'insert', head - 1
        idx = cups.index(head - 1)
        thead = head
        repcount = 0
        while thead < runend-3:
          repcount +=1
          thead += 4
        repcount -= 1
        thead -= 4
        headrun = thead
        remainder = []
        thead += 4
        while thead <= runend:
          remainder.append(thead)
          thead += 1

        print 'Runto', headrun, repcount, remainder
        fourbit = [(head, headrun, 'four')]
        twobit = [(head+1, headrun+3, 'two')]
        theround += repeat
        newcups = remainder + cups[1:idx+1] + twobit + cups[idx+1:] + fourbit
      elif rtype == 'four':
        repeat = (runend - head) / 4 / 4
        print 'consume', repeat, 'times'
        print head, head + 4, head + 8, '...'
        thead = head
        while thead < runend:
          thead += 4

        print head + (4 * 4 * repeat)
        print thead
        raise 'WIP'
      else:
        raise 'Unhandled Type' + rtype
    return theround, newcups

  def result(self, rounds, dim):
    #cups = [3, 8, 9, 1, 2, 5, 4, 6, 7]
    cups = [9, 4, 2, 3, 8, 7, 6, 1, 5, (10,999999,'one'), 1000000]
    #subs = rounds / 100
    #for s in range(100):
    #  print '.'
    theround = 1
    for i in range(rounds):
      print 'move', theround
      #print cups
      theround, cups = self.play(cups, dim, theround)
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
  puz.result(1000000, 1000000)

class Puzzle:

  def process(self, text):
    lines = text.split('\n')
    self.depart = int(lines[0])
    busses = lines[1].split(',')
    offset = {}
    remainders = {}
    first = int(busses[0])
    for i in range(len(busses)):
      bus = busses[i]
      if bus != 'x':
        bus = int(bus)
        offset[bus] = i
        rem = bus - i
        while rem < 0:
          rem += first
        remainders[bus] = rem
    self.busses = filter(lambda b: b != 'x' and b !='\n',busses)
    self.busses = filter(lambda b: b != 'x' and b !='\n',busses)
    self.busses = map(lambda b: int(b), self.busses)
    self.offsets = offset
    self.remainders = remainders

  def next(self, bus):
    whole = (self.depart / bus) * bus
    if whole == self.depart:
      return whole
    else:
      return whole + bus

  def remfactor(self, bus):
    #print self.offsets
    offset = self.offsets[bus]
    first = self.busses[0]
    #  target = bus - offset
    #  while target < 0:
    #    target += first
    target = self.remainders[bus]
    #print first, bus, offset, target
    factor = 0
    for i in range(bus * first):
    #i = 00
    #while True:
      i = i + 1
      mult = i * first
      div = mult / bus
      rem = (mult % bus)
      if (mult % bus) == target:
        print i, '*', first, '=', mult, ' = ', div, '*', bus, ' r', rem, ' vs ', target
        return div
    raise 'Bugger'

  def result1(self):
    earliest = None
    target = None
    for bus in self.busses:
      n = self.next(bus)
      if earliest:
        if earliest > n:
          earliest = n
          target = bus
      else:
        earliest = n
        target = bus
      print "Bus", bus, '->', n
    wait = earliest - self.depart
    print "Earliest:", target, '@', earliest, '-> ', wait, 'wait = ', target * wait 

  def intersect(self, a, b):
    shared = [value for value in a if value in b]
    return shared

  def result(self):
    mults = {}
    first = self.busses[0]
    for bus in self.busses:
      if not bus == self.busses[0]:
        fact = self.remfactor(bus)
        rem = self.remainders[bus]
        print fact
        nums = []
        for i in range(100000):
          #n = ((i * first) + fact ) * bus
          n = fact + (i*first)
          mult = (n * bus) + rem
          nums.append(mult)
        mults[bus] = nums

    common = mults[self.busses[1]]
    for bus in self.busses:
      if not bus == first:
        print mults[bus]
        common = self.intersect(common, mults[bus])
    print "Min Common Factor:", min(common)

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

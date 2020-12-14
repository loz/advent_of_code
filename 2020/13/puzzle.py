def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)

    for n_i, a_i in zip(n, a):
        print a_i, '(mod', n_i,')'
        p = prod / n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a / b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

#if __name__ == '__main__':
#    n = [3, 5, 7]
#    a = [2, 3, 2]
#    print chinese_remainder(n, a)


class Puzzle:

  def process(self, text):
    lines = text.split('\n')
    self.depart = int(lines[0])
    busses = lines[1].split(',')
    print busses
    offset = {}
    remainders = {}
    first = int(busses[0])
    for i in range(len(busses)):
      bus = busses[i]
      if bus != 'x':
        bus = int(bus)
        offset[bus] = i
        rem = bus - i
        print first, i, ':>', bus, '-', i, ' = ', rem, '->', rem % first
        remainders[bus] = rem % bus
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
        #print i, '*', first, '=', mult, ' = ', div, '* (', bus, ') r', rem, ' vs ', target
        print 'x =', rem, '(mod',  bus ,')'
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

  def result2(self):
    first = self.busses[0]
    for bus in self.busses:
      if not bus == self.busses[0]:
        fact = self.remfactor(bus)
        rem = self.remainders[bus]
    print 'Generating'
    initial = True
    common = []
    itter = 10000
    for bus in self.busses:
      if not bus == self.busses[0]:
        fact = self.remfactor(bus)
        rem = self.remainders[bus]
        print '.', 
        maxx = fact + ((itter * first) * bus) + rem
        print "max,", maxx
        if initial:
          for i in range(itter):
            n = fact + (i*first)
            mult = (n * bus) + rem
            common.append(mult)
          initial = False
        else:
          newcommon = []
          for i in range(itter):
            n = fact + (i*first)
            mult = (n * bus) + rem
            if mult in common:
              newcommon.append(mult)
          common = newcommon
    print "Min Common Factor:", min(common)

  def extended_gcd(self,a,b):
    (old_r, r) = (a, b)
    (old_s, s) = (1, 0)
    (old_t, t) = (0, 1)

    while r != 0:
      q = old_r / r
      (old_r, r) = (r, old_r - (q*r))
      (old_s, s) = (s, old_s - (q*s))
      (old_t, t) = (t, old_t - (q*t))
    #print "Co-effiencients", old_s, old_t
    #print "GCD", old_r
    #print "Quotients by GCD", t, s
    return (old_s, old_t)

  def result3(self):
    self.extended_gcd(17,13)
    self.extended_gcd(102*13,19)
    pairs = []
    for key in self.remainders:
      pairs.append((key, self.remainders[key]))
    print self.busses
    upper = 1
    for bus in self.busses:
      upper *= bus
    print "Upper Search:", upper
    print pairs
    pairs.sort(key=lambda p: p[0])
    print pairs
    last = pairs.pop(0)
    print last
    print "====="
    modd, _ = last 
    for pair in pairs:
      print last, pair
      lm, lr = last
      cm, cr = pair
      #if cr == 0:
      #  cr == cm
      (cl, cc) = self.extended_gcd(lm, cm)
      print cl, cc
      print lr, '*', cm, '*', cc, '+', cr, '*', lm, '*', cl
      n = (lr * cm * cc) + (cr * lm * cl)
      modd = modd * cm
      modd = lm * cm
      print '-> ', n, '%', modd
      n = n % modd
      print '-> ', n
      last = (n * cm, n *cl)
      print "=========="
    print n % upper

  def result(self):
    print self.busses
    print self.remainders
    pairs = []
    for key in self.remainders:
      pairs.append((key, self.remainders[key]))
    pairs.sort(key=lambda p: p[0])
    n = []
    a = []
    for pair in pairs:
      key, rem = pair
      n.append(key)
      a.append(rem)
    print chinese_remainder(n,a)

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

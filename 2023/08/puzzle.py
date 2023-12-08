import sys
from functools import reduce

DIRMAP = {
  'L' : 0,
  'R' : 1
}

def chinese_remainder(n, a):
    sum = 0
    prod = int(reduce(lambda a, b: a*b, n))

    print('Prod', prod)
    for n_i, a_i in zip(n, a):
        print(a_i, '(mod', n_i,')')
        p = int(prod / n_i)
        print(p)
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod

def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return
    while a > 1: # and b != 0:
        if b == 0:
          return x1
        #print('MV', a, b)
        q = int(a / b)
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

class Puzzle:

  def process(self, text):
    self.start = 'AAA'
    directions, *lines = text.split('\n')
    self.directions = [DIRMAP[ch] for ch in directions]
    self.current_dir = 0
    self.nodes = {}
    _, *lines = lines
    for line in lines:
      self.process_line(line)
    self.current = self.start

  def process_line(self, line):
    if line != '':
      node, rest = line.split(' = ')
      rest = rest.replace('(', '')
      rest = rest.replace(')', '')
      lhs, rhs = rest.split(', ')
      self.nodes[node] = (lhs, rhs)

  def walk(self):
    to, nd = self.walk_from(self.current, self.current_dir)
    self.current = to
    self.current_dir = nd
    return to

  def walk_from(self, ff, dd):
    d = self.directions[dd]
    dd = dd + 1
    if dd == len(self.directions):
      dd = 0
    nnext = self.nodes[ff]
    return (nnext[d], dd)


  def result(self):
    self.result2()

  def result2(self):
    starts = []
    for k in self.nodes.keys():
      if k.endswith('A'):
        starts.append(k)
    steps = 0
    ended = False
    current = starts
    direction = 0
    loop_data = []
    for start in starts:
      print('Checking Loops for', start)
      #Loop through until at same node again
      current = start
      direction = 0
      loops = 0
      while(loops < 3):
        zcount = 0
        count = 0
        ended = 0
        seen = {}
        while(not seen.get((current,direction), False)):
          seen[(current,direction)] = True
          if current.endswith('Z'):
            if ended == 0:
              ended = count
            zcount += 1
          count += 1
          current, direction = self.walk_from(current, direction)
        print('->', count, ' steps loop, hit Z after', ended, 'with', zcount, 'z conditions')
        loops = loops + 1
      loop_data.append((start, count, ended))
    self.optimised(loop_data)
    #self.brute_loops(loop_data)

  def optimised(self, loop_data):
    print(loop_data)
    pairs = []
    for loop in loop_data:
      o = loop[1]-loop[2]
      m = loop[2]
      pairs.append((o, m))
    pairs.sort(key=lambda x: x[0])
    n = []
    a = []
    print("Solve:")
    for pair in pairs:
      print(pair[0], " = n mod", pair[1])
      n.append(pair[1])
      a.append(pair[0])

    print(a)
    print(n)
    print(chinese_remainder(n,a))
    """
    a = [2, 2, 2, 3, 3, 4]
    n = [17619, 12359, 19197, 18670, 16040, 20773]
    print(a)
    print(n)
    #a = [2, 3, 4]
    #n = [17619 * 12359 * 19197, 18670 * 16040, 20773]

    done = False
    steps = 17619 * 12359 * 19197
    while(not done):
      done = True
      matches = []
      for n_i, a_i in zip(n, a):
        if (steps % n_i) == a_i:
          matches.append((n_i, a_i))
          #aprint('Step:', steps,  n_i, a_i)
        else:
          done = False
      if(len(matches) > 1):
        print('Step', steps, matches)
      steps = steps + 1

#2  = n mod 17619
#2  = n mod 12359
#2  = n mod 19197
#3  = n mod 18670
#3  = n mod 16040
#4  = n mod 20773
    #print(n, a)
    #print(chinese_remainder(n,a))
"""

  def brute_loops(self, loop_data):
    lmin = 9_999_999_999_999_999
    lloop = 0
    for loop in loop_data:
      print(loop, '=', loop[1]-loop[2])
      _, first, modo = loop
      if first < lmin:
        lmin = first
        lloop = modo
    print('Starting at', lmin, 'looping', lloop)
    val = lmin
    done = False
    while(not done):
      done = True
      text = '%s ' % (val)
      zcount = 0
      for loop in loop_data:
        label, s, lm = loop
        d = s-lm
        lv = val % lm
        if lv != d:
          done = False
        else:
          zcount = zcount + 1
          text = text + (', %s @ %d' % (label, lv))
      val += lloop
      if(zcount > 2):
        print(text)


    return
    done = False
    val = lmax
    while(not done):
      done = True
      num0 = 0
      text = "%s" % val
      for loop in loop_data:
        label, s, lm = loop
        lv = (val - s) % lm
        if lv != 0:
          done = False
        else:
          num0 = num0 + 1
        text = text + (', %s @ %d' % (label, lv))
      if(num0 > 2):
        print(text)
      val = val + lloop

  def result_brute(self):
    starts = []
    for k in self.nodes.keys():
      if k.endswith('A'):
        starts.append(k)
    steps = 0
    ended = False
    current = starts
    direction = 0
    while(not ended):
      ends = list(filter(lambda x: x.endswith('Z'), current))
      if(len(ends) > 2):
        print(current, ends, len(current), len(ends), '@', steps)
      if len(ends) == len(current):
        ended = True
        break
      nexts = []
      for loc in current:
        nnn, nd = self.walk_from(loc, direction)
        nexts.append(nnn)
      steps = steps + 1
      current = nexts
      direction = nd

    print('Steps', steps)

  def result1(self):
    print(self.start)
    current = self.start
    steps = 0
    while(current != 'ZZZ'):
      current = self.walk()
      print('->', current)
      steps = steps + 1
    print('Total', steps)



if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

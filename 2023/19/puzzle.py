import sys

class Puzzle:

  def process(self, text):
    self.rules = {}
    self.parts = []
    rules, parts = text.split('\n\n')

    for line in rules.split('\n'):
      self.process_rules(line)
    for line in parts.split('\n'):
      self.process_parts(line)

  def process_rules(self, line):
    if line != '':
      name, steps = line.split('{')
      steps = steps.replace('}', '')
      steps = steps.split(',')
      #print(name, steps)
      psteps = []
      for step in steps:
        if ':' in step:
          test, dest = step.split(':')
          if '>' in test:
            cmp = '>'
            var, val = test.split('>')
          else:
            cmp = '<'
            var, val = test.split('<')
          val = int(val)
          psteps.append( (var, cmp, val, dest) )
        else:
          psteps.append((None, step))
      self.rules[name] = psteps

  def process_parts(self, line):
    if line != '':
      line = line.replace('{','')
      line = line.replace('}','')
      part = {}
      vals = line.split(',')
      for v in vals:
        n, i = v.split('=')
        i = int(i)
        part[n] = i
      self.parts.append(part)

  def match(self, step, part):
    rules = self.rules[step]
    #print(step, rules, part)
    for rule in rules:
      #print('Rule', rule, len(rule))
      if rule[0] == None:
        return rule[1]
      var, cmp, val, dest = rule
      if cmp == '>':
        if part[var] > val:
          return dest
      else:
        if part[var] < val:
          return dest

  def r_map(self, steps, ranges):
    #incount = self.countrange(ranges)
    #print('Mapping', ranges, incount)
    mapped = []
    if len(steps) == 1:
      dest = steps[0][1]
      return [(dest, ranges)]
    rule, steps = steps[0], steps[1:]
    var, cmp, val, dest = rule
    a, b = ranges[var]
    #print(var, cmp, val, dest, ranges)
    rangea = {}
    rangeb = {}
    for k in ranges:
      rangea[k] = ranges[k]
      rangeb[k] = ranges[k]
    if cmp == '>':
      #X > (a..b)
      #if a > x -> all range (match)
      if a > val:
        return [(dest, ranges)]
      #if b > x -> new ranges a..x (rest), x+1..b (match)
      elif b > val:
        #(a..x)
        nrange = (a, val)
        rangea[var] = nrange
        #(x+1..b)
        nrange = (val+1, b)
        rangeb[var] = nrange
        return [(dest, rangeb)] + self.r_map(steps, rangea)
      #if x < a -> all range (rest)
      else:
        return self.r_map(steps, rangea)
    else:
      #print('<', rule, ranges)
      #X < (a..b)
      #if b < x -> all range (match)
      if b < val:
        return [(dest, ranges)]
      #if a < x -> new ranges a..x-1(match), x..b (rest)
      elif a < val:
        nrange = (a,  val-1)
        rangea[var] = nrange
        nrange = (val, b)
        rangeb[var] = nrange
        return [(dest, rangea)] + self.r_map(steps, rangeb)
      #if x > b -> all range (rest)
      else:
        return self.r_map(steps, rangea)

  def countrange(self, ranges):
    n = 1
    for k in ranges:
      a, b = ranges[k]
      n *= (b-a+1)
    return n

  def range_map(self, step, ranges):
    rules = self.rules[step]
    return self.r_map(rules, ranges)

  def result(self):
    self.result2()

  def result1(self):
    accepted = []
    rejected = []
    for part in self.parts:
      #print(part)
      step = 'in'
      while(step != 'A' and step != 'R'):
        step = self.match(step, part)
      if step == 'A':
        accepted.append(part)
      else:
        rejected.append(part)
    print('Accepted:')
    total = 0
    for part in accepted:
      score = part['x'] + part['m'] + part['a'] + part['s']
      print(part, score)
      total += score
    print('Total', total)
      
  def result2(self):
    accepted = []
    rejected = []
    state = ('in', {'x':(1,4000), 'm':(1,4000), 'a':(1,4000), 's':(1,4000)})
    toexplore = [state]
    while(toexplore):
      step, ranges = toexplore.pop(0)
      print('Exploring:', step, ranges)
      mapped = self.range_map(step, ranges)
      for state, mrange in mapped:
        if state == 'R':
          rejected.append(mrange)
          print('Rejecting', mrange)
        elif state == 'A':
          accepted.append(mrange)
          print('Accepting', mrange)
        else:
          #Explore
          toexplore.append((state, mrange))

    total = 0
    print()
    print('ranges:')
    for parts in accepted:
      x = (parts['x'][1]-parts['x'][0])+1
      m = (parts['m'][1]-parts['m'][0])+1
      a = (parts['a'][1]-parts['a'][0])+1
      s = (parts['s'][1]-parts['s'][0])+1
      score = x * m * a * s
      print(parts, ':', x, '*', m, '*', a, '*', s, '=', score)
      total += score
    print('total', total)
    print()
    print('Rejected:')
    complete = total
    total = 0
    for parts in rejected:
      x = (parts['x'][1]-parts['x'][0])+1
      m = (parts['m'][1]-parts['m'][0])+1
      a = (parts['a'][1]-parts['a'][0])+1
      s = (parts['s'][1]-parts['s'][0])+1
      score = x * m * a * s
      print(parts, ':', x, '*', m, '*', a, '*', s, '=', score)
      total += score
    print('total', total)
    print(total + complete, 'Parts accounted for')


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

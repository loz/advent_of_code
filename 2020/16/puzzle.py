class Puzzle:

  def process(self, text):
    lines = text.split('\n')
    fields = {}
    line = lines.pop(0)
    while line.strip() != '':
      field, ranges = self.parse_field(line)
      fields[field] = ranges
      line = lines.pop(0)
    self.fields = fields
    
    lines.pop(0) #your ticket:
    nums = lines.pop(0)
    self.yours = self.parse_nums(nums)
    
    lines.pop(0) #
    lines.pop(0) #nearby tickets
    others = []
    for line in lines:
      if line.strip() != '':
        others.append(self.parse_nums(line))
    self.others = others

  def parse_nums(self, nums):
    nums = nums.split(',')
    return map(lambda n: int(n), nums)

  def parse_range(self, rangetxt):
    bounds=rangetxt.rsplit('-')
    low = int(bounds[0])
    upp = int(bounds[1])
    return range(low,upp+1)

  def parse_field(self, line):
    name, rules = line.split(': ')
    rules = rules.split(' or ')
    rules = map(self.parse_range, rules)
    return (name, rules)
 
  def validField(self, field, num):
    ranges = self.fields[field]
    for r in ranges:
      if num in r:
        return True
    return False

  def valid(self, num):
    for i in self.fields:
      ranges = self.fields[i]
      for r in ranges:
        if num in r:
          return True
    return False

  def result(self):
    numvalid = 0
    numinvalid = 0
    total = 0
    for ticket in self.others:
      valid = True
      for num in ticket:
        if not self.valid(num):
          total += num
          valid = False
      if valid:
        numvalid += 1
      else:
        numinvalid += 1
      print ticket, valid
    print 'Valid', numvalid
    print 'Invalid', numinvalid
    print 'Error', total

  def _remove(self, ll, item):
    return filter(lambda i: i != item, ll)

  def result2(self):
    possfields = self.fields.keys()
    print possfields
    num = len(possfields)
    matches = []
    for n in range(num):
      print 'Searching for field', n
      considered = list(possfields)
      matched = []
      for field in considered:
        valid = True
        for ticket in self.others:
          if self.valid(ticket[n]):
            if not self.validField(field, ticket[n]):
              valid = False
        if valid:
          matched.append(field)
      #print matched
      matches.append((n, matched))
    print 'Narrowing'
    mapped = {}
    while len(matches) != 0:
      ones = filter(lambda m: len(m[1]) == 1, matches)
      rest = filter(lambda m: len(m[1]) != 1, matches)
      for one in ones:
        col, fields = one
        field = fields[0] #only 1
        print col, 'maps to', field
        mapped[field] = col
        #remove from consideration
        rest = map(lambda r: (r[0], self._remove(r[1],field)), rest)
      matches = rest
    
    print "======= YOUR TICKET ======="
    mult = 1
    for field in possfields:
      num = self.yours[mapped[field]]
      if field.startswith('departure'):
        mult *= num
      print field, ':', num
    print "==========================="
    print mult

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result2()

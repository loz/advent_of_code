class Puzzle:

  def process(self, text):
    lines = text.split('\n')
    line = lines.pop(0)
    self.rules = {}
    while line.strip() != '':
      id, rule = self.parse_rule(line)
      self.rules[id] = rule
      line = lines.pop(0)
    self.messages = filter(lambda l: l.strip() != '', lines)

  def parse_part(self, part):
    if part.startswith('"'):
      return part.replace('"', '')
    else:
      return map(lambda n: int(n), part.split(' '))

  def parse_rule(self, line):
    id, rest = line.split(': ')
    parts = rest.split(' | ')
    rules = map(lambda p: self.parse_part(p), parts)
    id = int(id)
    return (id, rules)

  def matches(self, ruleid, string):
    matched, rest = self._matches(ruleid, string, indent='')
    return (matched and rest == '')
  
  def _matches(self, ruleid, string, indent):
    print indent, 'MATCH:', ruleid, string
    if string == '':
      return (False, '')
    options = self.rules[ruleid]
    for option in options:
      oindent = str(option)
      if option == 'a' or option == 'b':
        if string[0] == option:
          return (True, string[1:])
        else:
          return (False, string)
      else:
        rest = string
        matched = True
        for rule in option:
          if matched:
            match, rest = self._matches(rule, rest, indent+' '+oindent)
            matched = matched and match
        if matched:
          return (True, rest)
    return (False, string)

  def adjust_rules(self):
    #self.rules[8] =  [[42, 8], [42]]
    #self.rules[11] = [[42,11,31], [42,31]]
    pass

  def result(self):
    total = 0
    for message in self.messages:
      matched = self.matches(0, message)
      if matched:
        total += 1
      print message, matched
    print 'Total Matched', total
    pass

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.adjust_rules()
  puz.result()

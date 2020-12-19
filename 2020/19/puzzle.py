import copy
import regex as re

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
    matched, rest, unexplored = self._matches(ruleid, string, indent='')
    return (matched and rest == '')
  
  def _matches(self, ruleid, string, indent):
    print indent, 'MATCH:', ruleid, string
    if string == '':
      return (False, '', None)
    options = self.rules[ruleid]
    unexplored = copy.copy(options)
    while len(unexplored) > 0:
      option = unexplored.pop(0)
      oindent = str(option)
      if option == 'a' or option == 'b':
        if string[0] == option:
          return (True, string[1:], unexplored)
        else:
          return (False, string, None)
      else:
        rest = string
        matched = True
        for rule in option:
          if matched:
            match, rest, unex = self._matches(rule, rest, indent+' '+oindent)
            print 'Unexplored', unex
            matched = matched and match
        if matched:
          return (True, rest, unexplored)
    return (False, string, None)

  def expand(self, ruleid, indent=''):
    options = self.rules[ruleid]
    #print indent, ruleid, options
    mapped = []
    for option in options:
      if option == 'a' or option == 'b':
        mapped.append(option)
      else:
        mapped_rules = map(lambda o: self.expand(o, indent + ' '), option)
        #print mapped_rules, '|' in mapped_rules
        mapped.append(''.join(mapped_rules))
    return '(' + '|'.join(mapped) + ')'

  def adjust_rules(self):
    #self.rules[8] =  [[42], [42,8]]
    #self.rules[11] = [[42,31], [42,11,31]]
    #self.rules[8] =  [[42, 8], [42]]
    #self.rules[11] = [[42,11, 31], [42,31]]
    pass

  def result1(self):
    total = 0
    for message in self.messages:
      matched = self.matches(0, message)
      if matched:
        total += 1
      print message, matched
    print 'Total Matched', total

  def result(self):
    total = 0
    fails = 0
    reg42 = self.expand(42)
    reg31 = self.expand(31)
    # 8: 42 | 42 8 -> (42)+
    reg8 = '(' + reg42 + ')+'
    #11: 42 31 | 42 11 31
    """
      42 31
      42 42 31 31
      42 42 42 31 31 31
      42{n}31{n}
    """
    # 0: 8 11
    """
      42+42{n}31{n}
      42{2,}31+
      where 42{n}>31{m}
      
      42+4231
      42+42{2}31{2}
      42+42{3}31{3}
      42+42{4}31{4}
    """
    #reg11 = '(?P<fourtwo>(' + reg42 + ')+)(?P<threeone>(' + reg31 + ')+)'
    #reg11 = '(' + reg42 + reg31 + ')|' + '(('+ reg42 +'){2}(' + reg31 + '){2})|' + '(('+ reg42 +'){3}(' + reg31 + '){3})|' + '(('+ reg42 +'){4}(' + reg31 + '){4})'
    #regall = '(' + reg42 + ')+' + '(' + '(' + reg42 + reg31 + ')|' + '(('+ reg42 +'){2}(' + reg31 + '){2})|' + '(('+ reg42 +'){3}(' + reg31 + '){3})|' + '(('+ reg42 +'){4}(' + reg31 + '){4})'+ ')'
    print '42:', reg42
    print '31:', reg31
    #print ' 8:', reg8
    #print '11:', reg11
    regall = '(?P<fourtwo>('+ reg42 + ')+)(?P<threeone>(' + reg31 + ')+)'
    #regall = '(?P<fourtwo>('+ reg42 + '){2})(?P<threeone>(' + reg31 + '){1})'
    print ' 0:', regall
    compiled = re.compile(regall)
    print 'Compiled'
    for message in self.messages:
      matched = compiled.fullmatch(message)
      matches = bool(matched)
      #if matches:
      #  total += 1
      #else:
      #  fails += 1
      if matches:
        m42 = matched['fourtwo']
        m31 = matched['threeone']
        m42count = len(re.findall(reg42, m42))
        m31count = len(re.findall(reg31, m31))
        #print '42', m42, m42count
        #print '31', m31, m31count
        print m42count, 'v', m31count
        if m42count <= m31count:
          matches = False
          fails += 1
        else:
          total +=1
      else:
        fails += 1
      print message, matches
    print 'Total matched', total
    print 'Total failed:', fails

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.adjust_rules()
  puz.result()

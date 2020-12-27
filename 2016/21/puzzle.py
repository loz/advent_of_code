class Puzzle:

  def process(self, text):
    lines = text.split('\n')
    rules = []
    for line in lines:
      if line.strip() != '':
        rules.append(self.parse_rule(line))
    self.rules = rules

  def parse_rule(self, line):
    if line.startswith('swap position'):
      line = line.replace('swap position ', '')
      locs = line.split(' with position ')
      return ('swapp', int(locs[0]), int(locs[1]))
    elif line.startswith('swap letter'):
      line = line.replace('swap letter ', '')
      lets = line.split(' with letter ')
      return ('swapl', lets[0], lets[1])
    elif line.startswith('rotate based on'):
      letter = line.replace('rotate based on position of letter ', '')
      return ('rotatep', letter)
    elif line.startswith('rotate'):
      line = line.replace('rotate ', '').replace('steps', '').replace('step', '')
      parts = line.split(' ')
      return ('rotate', parts[0], int(parts[1]))
    elif line.startswith('reverse positions'):
      line = line.replace('reverse positions ', '')
      locs = line.split(' through ')
      return ('reversep', int(locs[0]), int(locs[1]))
    elif line.startswith('move position'):
      line = line.replace('move position', '')
      locs = line.split(' to position ')
      return ('move', int(locs[0]), int(locs[1]))

  def _swapper(self, x, a, b):
    if x == a: 
      return b
    elif x == b:
      return a
    else:
      return x

  def _apply(self, cyphertext, rules):
    cypher = [ch for ch in cyphertext]
    for rule in rules:
      #print rule, cypher
      rtype = rule[0]
      if rtype == 'swapp':
        _, a, b = rule
        ca = cypher[a]
        cypher[a] = cypher[b]
        cypher[b] = ca
      elif rtype == 'swapl':
        _, a, b = rule
        cypher = map(lambda x: self._swapper(x, a, b), cypher)
      elif rtype == 'rotate':
        _, d, size = rule
        if d == 'left':
          cypher = cypher[size:] + cypher[:size]
        else:
          l = len(cypher) - size
          cypher = cypher[l:] + cypher[:l]
      elif rtype == 'rotatep':
        _, letter = rule
        pos = cypher.index(letter)
        #print 'ROTATE', letter, '@', pos, cypher
        if pos >= 4:
          pos += 2
        else:
          pos += 1
        l = len(cypher) - pos
        cypher = cypher[l:] + cypher[:l]
      elif rtype == 'r_rotatep':
        """Forward
@0 -> R1 -> @1
@1 -> R2 -> @3
@2 -> R3 -> @5
@3 -> R4 -> @7
@4 -> R6 -> @10 -> 2
@5 -> R7 -> @12 -> 4
@6 -> R8 -> @14 -> 6
@7 -> R9 -> @16 -> 0"""
        reverse = {
          1: 1, 3: 2, 5: 3, 7: 4,
          2: 6, 4: 7, 6: 8, 0: 1
        }
        _, letter = rule
        pos = cypher.index(letter)
        l = reverse[pos]
        cypher = cypher[l:] + cypher[:l]
      elif rtype == 'reversep':
        _, start, finish = rule
        mid = cypher[start:finish+1]
        mid.reverse()
        cypher = cypher[0:start] + mid + cypher[finish+1:]
      elif rtype == 'move':
        _, start, finish = rule
        let = cypher[start]
        if start < finish:
          cypher = cypher[0:start] + cypher[start+1:finish+1] + [let] + cypher[finish+1:]
        else:
          cypher = cypher[0:finish] + [let] + cypher[finish:start] + cypher[start+1:]
    return ''.join(cypher)
    

  def encode(self, cyphertext):
    return self._apply(cyphertext, self.rules)

  def _reverse_rule(self, rule):
    #print 'Reverse', rule
    rtype = rule[0]
    if rtype == 'rotate':
      _, d, v = rule
      if d == 'left':
        rule = ('rotate', 'right', v)
      else:
        rule = ('rotate', 'left', v)
    elif rtype == 'move':
      _, a, b = rule
      rule = ('move', b, a)
    elif rtype == 'rotatep':
      _, ch = rule
      rule = ('r_rotatep', ch)
    #print '=', rule
    return rule

  def decode(self, cyphertext):
    rules = map(lambda x: self._reverse_rule(x), self.rules)
    rules.reverse()
    return self._apply(cyphertext, rules)
   

  def result(self, txt, txt2):
    print 'Encoding', txt
    print '======'
    etxt = self.encode(txt)
    print '=', etxt
    print 'decode ->', self.decode(etxt)
    print '========'
    print 'Decoding', txt2
    dtxt = self.decode(txt2)
    print '====='
    print '=', dtxt 
    print 'recode ->', self.encode(dtxt)

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result('abcdefgh', 'fbgdceah')

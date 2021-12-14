import math

class Puzzle:

  def process(self, text):
    lines = text.split('\n')
    self.process_chain(lines[0])
    lines = lines[2:]
    self.process_reactions(lines)
    self.build_pairs()

  def build_pairs(self):
    pairs = {}
    for c in range(len(self.chain)-1):
      pair = self.chain[c] + self.chain[c+1]
      pc = pairs.get(pair, 0)
      pc += 1
      pairs[pair] = pc
    self.pairs = pairs


  def process_chain(self, chain):
    chain = chain.rstrip()
    self.chain = [ch for ch in chain]

  def process_reactions(self, lines):
    reactions = {}
    for line in lines:
      if len(line) > 0:
        left, right = line.split(' -> ')
        reactions[left] = right
    self.reactions = reactions

  def expand_pairs(self):
    print self.pairs
    newpairs = {}
    for pair in self.pairs:
      pc = self.pairs[pair]
      if pc > 0:
        #print pc, self.reactions[pair]
        r = self.reactions[pair]
        left = pair[0]
        right = pair[1]
        nl = left + r
        nr = r + right
        newpairs[nl] = newpairs.get(nl, 0) + pc
        newpairs[nr] = newpairs.get(nr, 0) + pc
    self.pairs = newpairs
        

  def expand(self):
    newchain = []
    for c in range(len(self.chain)-1):
      pair = self.chain[c] + self.chain[c+1]
      newchain.append(self.chain[c])
      newchain.append(self.reactions[pair])
    newchain.append(self.chain[c+1])
    self.chain = newchain

  def pair_freqs(self):
    freqs = {}
    print self.pairs
    for pair in self.pairs:
      l = pair[0]
      r = pair[1]
      freqs[l] = freqs.get(l, 0) + self.pairs[pair]
      freqs[r] = freqs.get(r, 0) + self.pairs[pair]
    for freq in freqs:
      freqs[freq] = math.ceil(freqs[freq]/2.0)
    return freqs

  def freqs(self):
    freqs = {}
    for c in self.chain:
      fc = freqs.get(c, 0)
      fc += 1
      freqs[c] = fc
    return freqs
    
  def min_max(self, freqs):
    mmin = min(freqs.keys(), key=lambda f: freqs[f])
    mmax = max(freqs.keys(), key=lambda f: freqs[f])
    return ((mmin, freqs[mmin]), (mmax, freqs[mmax]))

  def chain_string(self):
    return ''.join(self.chain)

  def result(self):
    for s in range(40):
      print 'Step', s
      print self.pair_freqs()
      #print self.min_max()
      self.expand_pairs()
    f = self.pair_freqs()
    print self.min_max(f)
    #print self.chain_string()
    #print self.min_max()

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

class Puzzle:

  def process(self, text):
    lines = text.split('\n')
    self.process_chain(lines[0])
    lines = lines[2:]
    self.process_reactions(lines)

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

  def expand(self):
    newchain = []
    for c in range(len(self.chain)-1):
      pair = self.chain[c] + self.chain[c+1]
      newchain.append(self.chain[c])
      newchain.append(self.reactions[pair])
    newchain.append(self.chain[c+1])
    self.chain = newchain

  def min_max(self):
    freqs = {}
    for c in self.chain:
      fc = freqs.get(c, 0)
      fc += 1
      freqs[c] = fc
    mmin = min(freqs.keys(), key=lambda f: freqs[f])
    mmax = max(freqs.keys(), key=lambda f: freqs[f])
    return ((mmin, freqs[mmin]), (mmax, freqs[mmax]))

  def chain_string(self):
    return ''.join(self.chain)

  def result(self):
    for s in range(10):
      self.expand()
    print self.chain_string()
    print self.min_max()

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

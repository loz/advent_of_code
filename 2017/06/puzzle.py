import copy

class Puzzle:

  def process(self, text):
    self.memory = []
    chunks = text.split()
    for chunk in chunks:
      self.memory.append(int(chunk))
    self.size = len(self.memory)

  def defrag(self):
    chunk = max(self.memory)
    idx = self.memory.index(chunk)
    self.memory[idx] = 0
    while chunk > 0:
      idx += 1
      idx = idx % self.size
      self.memory[idx] += 1
      chunk -= 1

  def result(self):
    seen = {}
    steps = 0
    hkey = ','.join(map(lambda m: str(m), self.memory))
    while not seen.has_key(hkey):
      seen[hkey] = steps
      print steps, self.memory
      self.defrag()
      steps +=1 
      hkey = ','.join(map(lambda m: str(m), self.memory))
    print 'Total Before repeat', steps
    print self.memory
    hkey = ','.join(map(lambda m: str(m), self.memory))
    print 'Last Seen', seen[hkey]
    print 'Loop = ', steps-seen[hkey]

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

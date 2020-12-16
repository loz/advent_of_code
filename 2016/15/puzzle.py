import re

PHRASE = r"Disc #(\d+) has (\d+) positions; at time=(\d+), it is at position (\d+)."

class Puzzle:

  def process(self, text):
    lines = text.split('\n')
    self.discs = {}
    self.time = 0
    for line in lines:
      if line.strip() != '':
        parts = self.parse(line)
        num, pcount, t, tpos = parts
        self.discs[num] = {'count': pcount, 'time': t, 'tpos': tpos}

  def position(self, time, num):
    disc = self.discs[num]
    t0 = disc['time']
    count = disc['count']
    tpos = disc['tpos']
    time = time - t0
    #print 't0', t0, 'time', time, 'count', count
    pos = time % count
    pos = pos + tpos
    pos = pos % count
    return pos

  def parse(self, line):
    match = re.match(PHRASE, line)
    return map(lambda m: int(m), match.groups())

  def result(self):
    time = 0
    while True:
      #print 'Time t =', time
      dt = time
      broke = False
      for num in self.discs:
        dt = dt + 1
        dpos = self.position(dt, num)
        if dpos != 0:
          broke = True
          break
        #print num, dpos
      #print 'Did Break?', broke
      if not broke:
        print 'Time t =', time
        print 'Found!'
        exit()
      time += 1
      #exit()
    pass

  def addDisk(self):
    print self.discs
    newid = max(self.discs.keys()) + 1
    print newid
    self.discs[newid] = {'count': 11, 'time': 0, 'tpos': 0}
    print self.discs

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.addDisk()
  puz.result()

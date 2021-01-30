class Puzzle:

  def process(self, text):
    self.ranges = {}
    self.captures = []
    self.positions = {}
    self.directions = {}
    self.packet_loc = -1
    lines = text.split('\n')
    for line in lines:
      if line.strip() != '':
        self.process_line(line)

  def process_line(self, line):
    parts = line.split(':')
    dval, rval = parts
    dval = int(dval.strip())
    rval = int(rval.strip())
    self.ranges[dval] = rval
    self.positions[dval] = 0
    self.directions[dval] = -1

  def tick(self):
    self.packet_loc += 1
    if self.ranges.has_key(self.packet_loc) and self.positions[self.packet_loc] == 0:
      self.captures.append(self.packet_loc)
    for depth in self.ranges:
      if self.positions[depth] == self.ranges[depth] - 1 or self.positions[depth] == 0:
        self.directions[depth] = 0 - self.directions[depth]
      self.positions[depth] += self.directions[depth]

  def reset(self):
    self.packet_loc = -1
    self.captures = []
    for depth in self.ranges:
      self.positions[depth] = 0
      self.directions[depth] = -1

  def result1(self):
    maxdepth = max(self.ranges.keys())
    print 'Max Depth', maxdepth
    for d in range(maxdepth+1):
      self.tick()
    print 'Hits:'
    for depth in self.captures:
      print depth
    print 'Severity:', self.severity()

  def result(self):
    sev = -100
    delay = 0
    while sev != 0:
      delay += 2
      sev = self.runwait(delay)

  def runwait(self, delay):
    self.reset()
    self.packet_loc -= delay
    maxdepth = max(self.ranges.keys())
    print 'Delay %d' % delay,
    for d in range(maxdepth+1 + delay):
      self.tick()
    sev = self.severity()
    print '-> Severity:', sev
    return sev

  def hits(self):
    return self.captures

  def severity(self):
    sev = 0
    for depth in self.captures:
      sev += (self.ranges[depth] * depth)
    return sev

  def depth(self, depth):
    return self.ranges[depth]

  def scannerAt(self, depth):
    return self.positions[depth]

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

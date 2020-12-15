class Puzzle:

  def process(self, num):
    self.favorite = num

  def generate(self, x, y):
    num = (x*x) + (3*x) + (2*x*y) + y + (y*y) + self.favorite
    bin = "{0:b}".format(num)
    count = 0
    for ch in bin:
      if ch == '1':
        count += 1
    #print num, bin, count
    if (count % 2) == 0:
      return '.'
    else:
      return '#'

  def print_map(self, width, height):
    for y in range(0, height):
      line = ''
      for x in range(0, width):
        line += self.generate(x, y)
      print line
      line = ''

  def print_trace(self, width, height, visited):
    for y in range(0, height):
      line = ''
      for x in range(0, width):
        if visited.has_key((x,y)):
          line += '\033[96mO\033[0m'
        else:
          line += self.generate(x, y)
      print line
      line = ''

  def generate_neighbours(self, loc):
    x, y = loc
    deltas = [(0,-1), (0, 1), (-1, 0), (1, 0)]
    locs = []
    for d in deltas:
      dx, dy = d
      nx = x + dx
      ny = y + dy
      if nx >= 0 and ny >= 0:
        locs.append(((nx,ny), self.generate(nx, ny)))
    return locs

  def result(self, target):
    print 'Searching for', target
    visited = {}
    generated = {(1,1):'.'}
    head = [(1,1)]
    distance = 0
    tail = []
    while len(head) > 0:
      loc = head.pop()
      visited[loc] = True
      neighbours = self.generate_neighbours(loc)
      if loc == target:
        print 'Target Reached @', distance
        exit()
      for n in neighbours:
        nloc, gen = n
        if not generated.has_key(nloc):
          generated[nloc] = gen
          if gen == '.':
            tail.append(nloc)
      if len(head) == 0:
        distance += 1
        print ""
        self.print_trace(40,40, visited)
        head = tail
        tail = []

  def result2(self):
    visited = {}
    generated = {(1,1):'.'}
    head = [(1,1)]
    distance = 0
    tail = []
    while len(head) > 0:
      if distance == 51:
        print 'Target Reached @', distance
        print 'Reached', len(visited.keys())
        exit()
      loc = head.pop()
      visited[loc] = True
      neighbours = self.generate_neighbours(loc)
      for n in neighbours:
        nloc, gen = n
        if not generated.has_key(nloc):
          generated[nloc] = gen
          if gen == '.':
            tail.append(nloc)
      if len(head) == 0:
        print "Distance", distance, len(visited.keys())
        distance += 1
        self.print_trace(40,30, visited)
        head = tail
        tail = []
    

if __name__ == '__main__':
  puz = Puzzle()
  puz.process(1358)
  #puz.result((31,39))
  puz.result2()

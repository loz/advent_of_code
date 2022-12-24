import sys
from collections import defaultdict
import heapq

DELTAS = [
  (-1, 0),
  ( 1, 0),
  (0, -1),
  (0, 1)
]
class Puzzle:

  def process(self, text):
    self.start = (1,0)
    self.height = 0
    self.r_blizards = defaultdict(list)
    self.u_blizards = defaultdict(list)
    self.l_blizards = defaultdict(list)
    self.d_blizards = defaultdict(list)

    for line in text.split('\n'):
      self.process_line(line)
    self.end = (self.width-2, self.height-1)

  def process_line(self, line):
    if line != '':
      self.width = len(line)
      for x in range(self.width):
        if line[x] == '>':
          self.r_blizards[self.height].append(x)
        elif line[x] == '<':
          self.l_blizards[self.height].append(x)
        elif line[x] == '^':
          self.u_blizards[x].append(self.height)
        elif line[x] == 'v':
          self.d_blizards[x].append(self.height)
      self.height+=1

  def blizard_at(self, loc, t=0):
    x, y = loc
    for b in self.r_blizards[y]:
      if ((b-1+t) % (self.width-2))+1 == x:
        return True
    for b in self.l_blizards[y]:
      if ((b-1-t) % (self.width-2))+1 == x:
        return True
    for b in self.u_blizards[x]:
      if ((b-1-t) % (self.height-2))+1 == y:
        return True
    for b in self.d_blizards[x]:
      #height->5, m = 5-2
      #2@2 -> 3 -> 1 = (2-1+2) % m + 1 = 3 % m +1 = 0 + 1
      if ((b-1+t) % (self.height-2))+1 == y:
        return True
    return False

  def options(self, loc, t):
    options = []
    x, y = loc
    for d in DELTAS:
      dx, dy = d
      nx = x+dx
      ny = y+dy
      if (nx,ny) == self.end or (nx,ny) == self.start:
        pass #return [(nx,ny)]
      else:
        if nx <= 0 or nx >= self.width-1:
          continue
        if ny <= 0 or ny >= self.height-1:
          continue
        if self.blizard_at((nx,ny), t):
          continue
      options.append((nx, ny))
    #Wait here if not hit by blizard
    if not self.blizard_at(loc, t):
      options.append(loc)
    return options

  def a_h(self, a, b):
    ax, ay = a
    bx, by = b
    return abs(bx-ax) + abs(by-ay)

  def astar(self, start, end, t_start):
    g_score = defaultdict(lambda: sys.maxsize)
    f_score = defaultdict(lambda: sys.maxsize)
    g_score[(start, t_start)] = 0
    start_h = self.a_h(start, end)
    f_score[(start, t_start)] = start_h
    pq = []
    heapq.heapify(pq)
    heapq.heappush(pq, [(start_h, start_h), (start, t_start)])
    paths = {}
    #depth = 0
    while pq:
      #depth += 1
      score, loc = heapq.heappop(pq)
      pos, t = loc
      #if depth % 100000 == 0:
      #  print 'Check', loc, t
      #  self.dump(pos, t)
      #  return
      #print score, loc
      if pos == end:
        print 'Reached Exit', t
        break
      options = self.options(pos,t+1)
      for option in options:
        g_s = g_score[loc]+1
        a_h = self.a_h(option, end)
        f_s = g_s + a_h

        if f_s < f_score[(option,t+1)]:
          g_score[(option,t+1)] = g_s
          f_score[(option,t+1)] = f_s
          heapq.heappush(pq, [(f_s, a_h), (option, t+1)])
          paths[(option, t+1)] = loc

    fwdpath = {}
    node = (end, t)
    while node != (start, t_start):
      fwdpath[paths[node]] = node
      node = paths[node]
    return fwdpath

  def dump(self, pos, t):
    for y in range(self.height):
      for x in range(self.width):
        if self.blizard_at((x,y), t):
          sys.stdout.write('*')
        elif (x,y) == pos:
          sys.stdout.write('E')
        elif (x,y) == self.start or (x,y) == self.end:
          sys.stdout.write('.')
        elif x == 0 or x == self.width-1:
          sys.stdout.write('#')
        elif y == 0 or y == self.height-1:
          sys.stdout.write('#')
        else:
          sys.stdout.write('.')
      print

  def result1(self):
    path = self.astar(self.start, self.end, 0)
    t = 0
    pos = self.start
    #self.dump(pos, t)
    while pos != self.end:
      pos, t = path[(pos, t)]
      #print 'Minute ', t, pos
      #self.dump(pos, t)
      #print
    print 'Moves', len(path)

  def result(self):
    path = self.astar(self.start, self.end, 0)
    out = len(path)
    print 'Start -> Goal' , out
    path = self.astar(self.end, self.start, out)
    back = len(path)
    path = self.astar(self.start, self.end, out+back)
    goal = len(path)
    print 'Goal -> Start', back
    print 'Start -> Goal', goal
    print 'Total', out + back + goal


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

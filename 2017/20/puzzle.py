import sys
from itertools import combinations

class Particle:
  def __init__(self, p, v, a, idx):
    self.p = p
    self.v = v
    self.a = a
    self.idx = idx
    self.current_distance = None
    self.calculateDistance()

  def dump(self):
    print self.idx, ': p=', self.p, 'v=', self.v, 'a=', self.a, 'Distance: ', self.last_distance, '->', self.current_distance

  def calculateDistance(self):
    self.last_distance = self.current_distance
    self.current_distance = abs(self.p[0]) + abs(self.p[1]) + abs(self.p[2])

  def simulate(self):
    ax, ay, az = self.a
    vx, vy, vz = self.v
    px, py, pz = self.p
    vx += ax
    vy += ay
    vz += az

    px += vx
    py += vy
    pz += vz

    self.v = (vx, vy, vz)
    self.p = (px, py, pz)
    self.calculateDistance()

class Puzzle:

  def process(self, text):
    self.particles = []

    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      parts = line.split(', ')
      p = self.parse_values(parts[0])
      v = self.parse_values(parts[1])
      a = self.parse_values(parts[2])
      idx = len(self.particles)
      self.particles.append(Particle(p, v, a, idx))

  def parse_values(self, chunk):
    trimmed = chunk[3:]
    trimmed = trimmed[0:-1]
    parts = trimmed.split(',')
    return (int(parts[0]), int(parts[1]), int(parts[2]))

  def result1(self):
    slowest_acc = min(self.particles, key=lambda x: abs(x.a[0]) + abs(x.a[1]) + abs(x.a[2]))
    slowest_acc.dump()

  def result(self):
    survivors = self.particles
    for n in range(100):
      seen = {}
      collisions = set()
      for p in survivors:
        p.simulate()
        pp = seen.get(p.p, [])
        pp.append(p)
        seen[p.p] = pp
      
      for sets in seen:
        if len(seen[sets]) > 1:
          print 'Collisions!', seen[sets]
          for p in seen[sets]:
            survivors.remove(p)
      print len(survivors), 'Remaining'



if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

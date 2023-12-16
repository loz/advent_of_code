import sys

class Puzzle:

  def process(self, text):
    self.grid = []
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      self.grid.append([ch for ch in line])

  def at(self, x, y):
    if x < 0 or y < 0 or x >= len(self.grid[0])  or y >= len(self.grid):
      return None
    return self.grid[y][x]

  def beam(self, d, loc):
    x, y = loc
    outs = []
    val = self.at(x, y)
    if d == 'r':
      if val == '.' or val == '-':
        outs.append(('r', (x+1, y)))
      elif val == '\\':
        outs.append(('d', (x, y+1)))
      elif val == '/':
        outs.append(('u', (x, y-1)))
      elif val == '|':
        outs.append(('u', (x, y-1)))
        outs.append(('d', (x, y+1)))
    elif d == 'l':
      if val == '.' or val == '-':
        outs.append(('l', (x-1, y)))
      elif val == '\\':
        outs.append(('u', (x, y-1)))
      elif val == '/':
        outs.append(('d', (x, y+1)))
      elif val == '|':
        outs.append(('u', (x, y-1)))
        outs.append(('d', (x, y+1)))
    elif d == 'd':
      if val == '.' or val == '|':
        outs.append(('d', (x, y+1)))
      elif val == '\\':
        outs.append(('r', (x+1, y)))
      elif val == '/':
        outs.append(('l', (x-1, y)))
      elif val == '-':
        outs.append(('l', (x-1, y)))
        outs.append(('r', (x+1, y)))
    else:
      if val == '.' or val == '|':
        outs.append(('u', (x, y-1)))
      elif val == '\\':
        outs.append(('l', (x-1, y)))
      elif val == '/':
        outs.append(('r', (x+1, y)))
      elif val == '-':
        outs.append(('l', (x-1, y)))
        outs.append(('r', (x+1, y)))

    return outs

  def result(self):
    self.result2()

  def result2(self):
    options = []
    xm = len(self.grid[0])
    ym = len(self.grid)
    for x in range(xm):
      options.append(('d', (x, 0)))
      options.append(('u', (x, ym)))
    for y in range(ym):
      options.append(('r', (0, y)))
      options.append(('l', (xm, y)))
    print(options)
    
    best = None
    bmax = 0
    while options:
      current = options.pop(0)
      sys.stdout.write('Scanning.. %d remaining' % len(options))
      litcount, lights = self.explore(current)
      if litcount > bmax:
        print('-> New Best -> ', litcount)
        bmax = litcount
        best = lights
      else:
        print(' ->', litcount)
    self.dump_lights(best)

  def explore(self, start):
    light = {}
    explore = [start]
    visited = {}
    while explore:
      current = explore.pop(0)
      if current not in visited:
        #print('Exploring', current)
        visited[current] = True
        d, loc = current
        isvalid = self.at(loc[0], loc[1])
        if isvalid != None:
          cl = light.get(loc, 0)
          cl += 1
          light[loc] = cl
          outs = self.beam(d, loc)
          for o in outs:
            explore.append(o)
    return (len(light.keys()), light)


  def result1(self):
    light = {}
    explore = [('r', (0, 0))]
    visited = []
    while explore:
    #for x in range(10):
      current = explore.pop(0)
      if current not in visited:
        #print('Exploring', current)
        visited.append(current)
        d, loc = current
        isvalid = self.at(loc[0], loc[1])
        if isvalid != None:
          cl = light.get(loc, 0)
          cl += 1
          light[loc] = cl
          outs = self.beam(d, loc)
          for o in outs:
            explore.append(o)
    self.dump_lights(light)

  def dump_lights(self, lights):
    #Print the grid
    total = 0
    for y, row in enumerate(self.grid):
      for x, ch in enumerate(row):
        #if ch in "|/\\-":
        #  sys.stdout.write(ch)
        #else:
          l = lights.get((x, y), 0)
          if l > 0:
            total += 1
            sys.stdout.write('#')
          else:
            sys.stdout.write('.')
      sys.stdout.write('\n')
    print('Total Lit:', total)

if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

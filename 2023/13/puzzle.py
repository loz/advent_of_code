import sys

class Puzzle:
  class Grid:
    def __init__(self, chunk):
      self.data = []
      for line in chunk.split('\n'):
        if line != '':
          self.data.append(line)
      self.height = len(self.data)
      self.width = len(self.data[0])

    def dump(self):
      print('\n'.join(self.data))

    def hreflect(self):
      for l in range(self.width-1):
        #print('Trying', l)
        lhs = self.data[0][:l+1]
        rhs = self.data[0][l+1:]
        w = min(len(lhs), len(rhs))
        matched = True
        for row in self.data:
          lhs = row[:l+1]
          rhs = row[l+1:]
          #Clamp
          lhs = lhs[0-w:]
          rhs = rhs[:w]
          rhs = rhs[::-1]
          #print(lhs, ' | ', rhs)
          if lhs != rhs:
            matched = False
            break
        #print('Didmatch', matched)
        if(matched):
          return (l+1, l+2)
      return None

    def cell_diff(self, a, b):
      total = 0
      for x in range(len(a)):
        if a[x] != b[x]:
          total += 1
      return total

    def smudge_hreflect(self):
      for l in range(self.width-1):
        #print('Trying', l)
        lhs = self.data[0][:l+1]
        rhs = self.data[0][l+1:]
        w = min(len(lhs), len(rhs))
        matched = True
        td = 0
        for row in self.data:
          lhs = row[:l+1]
          rhs = row[l+1:]
          #Clamp
          lhs = lhs[0-w:]
          rhs = rhs[:w]
          rhs = rhs[::-1]
          cd = self.cell_diff(lhs, rhs)
          td += cd
          #print(lhs, ' | ', rhs, ' >>', cd)
          if td > 1:
            matched = False
            break
        #print('Didmatch', matched)
        if(td == 1): #one cell diff
          return (l+1, l+2)
      return None

    def vreflect(self):
      for l in range(self.height-1):
        #print('Trying', l)
        top = self.data[:l+1]
        bot = self.data[l+1:]
        w = min(len(top), len(bot))
        top = top[0-w:]
        bot = bot[:w]
        bot = list(reversed(bot))
        #print(top, '\n ----- \n', bot)
        if top == bot:
          return (l+1, l+2)

      return None

    def row_cell_diff(self, a, b):
      td = 0
      for x in range(len(a)):
        td += self.cell_diff(a[x], b[x])
      return td

    def smudge_vreflect(self):
      for l in range(self.height-1):
        #print('Trying', l)
        top = self.data[:l+1]
        bot = self.data[l+1:]
        w = min(len(top), len(bot))
        top = top[0-w:]
        bot = bot[:w]
        bot = list(reversed(bot))
        td = self.row_cell_diff(top, bot)
        #print(top, '\n ----- \n', bot, ' >>', td)
        if td == 1:
          return (l+1, l+2)

      return None

  def process(self, text):
    self.grids = []
    for chunk in text.split('\n\n'):
      self.process_set(chunk)

  def process_set(self, chunk):
    if chunk != '':
      grid = Puzzle.Grid(chunk)
      self.grids.append(grid)

  def result(self):
    self.result2()

  def result2(self):
    th = 0
    tv = 0
    for grid in self.grids:
      grid.dump()
      h = grid.smudge_hreflect()
      v = grid.smudge_vreflect()
      print('H', h, 'or V', v)
      if h:
        th += h[0]
      elif v:
        tv += v[0]
      print()
    print('Th', th, 'Tv', tv, ' Total', (100*tv)+th)

  def result1(self):
    th = 0
    tv = 0
    for grid in self.grids:
      grid.dump()
      h = grid.hreflect()
      v = grid.vreflect()
      print('H', h, 'or V', v)
      if h:
        th += h[0]
      elif v:
        tv += v[0]
      print()
    print('Th', th, 'Tv', tv, ' Total', (100*tv)+th)



if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

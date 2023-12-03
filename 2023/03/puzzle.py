import sys

class Puzzle:

  def process(self, text):
    self.schematic = []
    self.numbers = {}
    self.stars = []
    y = 0
    for line in text.split('\n'):
      if line != '':
        self.schematic.append(line)
        self.scan_line(y)
        y = y + 1

  def scan_line(self, ypos):
    row = self.schematic[ypos]
    num = ''
    inNum = False
    loc = -1
    for xpos in range(len(row)):
      ch = row[xpos]
      if ch in '0123456789':
        num += ch
        if not inNum:
          loc = xpos
          inNum = True
      else:
        if ch == '*':
          self.stars.append((xpos, ypos))
        if inNum:
          self.numbers[(loc,ypos)] = num
          inNum = False
          num = ''
          loc = -1
    if inNum:
      self.numbers[(loc,ypos)] = num

  def debug(self):
    for y in range(len(self.schematic)):
      for x in range(len(self.schematic[y])):
        ch = self.schematic[y][x]
        if self.at(x,y) and self.isPart(x,y):
          ch = "Y"
        sys.stdout.write(ch)
      sys.stdout.write("\n")

  def result(self):
    #self.debug()
    self.result2()

  def result2(self):
    total = 0
    starmap = {}
    #print(self.stars)
    for loc in self.numbers.keys():
      x, y = loc
      item = self.at(x,y)
      isP = self.isPart(x,y)
      ns = self.get_neighbours(x,y,len(item))
      if isP:
        #print(loc, item, isP, ns)
        for n in ns:
          if n in self.stars:
            sm = starmap.get(n, [])
            sm.append(item)
            starmap[n] = sm
    print('====')
    for s in self.stars:
      gears = starmap.get(s,None)
      print (s, gears)
      if gears and len(gears) == 2:
        g = int(gears[0]) * int(gears[1])
        total += g
        print("Gear", g)
    print('Total', total)

  def result1(self):
    total = 0
    for loc in self.numbers.keys():
      x, y = loc
      item = self.at(x,y)
      isP = self.isPart(x,y)
      ns = self.get_neighbours(x,y,len(item))
      print(loc, item, isP, ns)
      if isP:
        total = total + int(item)
    print('Total', total)

  def at(self, x, y):
    item = self.numbers.get((x,y), None)
    return item

  def isPart(self, x, y):
    item = self.at(x,y)
    neighbours = self.get_neighbours(x,y,len(item))
    if len(neighbours) > 0:
      return True
    return False
  
  def get_neighbours(self, sx, sy, xlen):
    ns = []
    for x in range(sx-1,sx+xlen+1):
      if x>=0 and x<len(self.schematic[0]):
        if sy>0:
          ch = self.schematic[sy-1][x]
          if ch not in ".0123456789":
            ns.append((x, sy-1))
    if sx+xlen<len(self.schematic[0]):
      ch = self.schematic[sy][sx+xlen]
      if ch not in ".0123456789":
        ns.append((sx+xlen,sy))
    if sx>0:
      ch = self.schematic[sy][sx-1]
      if ch not in ".0123456789":
        ns.append((sx-1,sy))
    for x in range(sx-1,sx+xlen+1):
      if x>=0 and x<len(self.schematic[0]):
        if sy<len(self.schematic)-1:
          ch = self.schematic[sy+1][x]
          if ch not in ".0123456789":
            ns.append((x,sy+1))
    return ns

if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

class Puzzle:
  
  def define(self, xrange, yrange):
    self.xrange = xrange
    self.yrange = yrange
    self.options = []
    self.calc_v_range()

  def calc_v_range(self):
    x = 1
    v = 1
    ranges = []
    while x <= self.xrange[1]:
      x+=v
      if x >= self.xrange[0] and x<= self.xrange[1]:
        #print 'V', v, x
        ranges.append(v)
      v+=1
    self.min_x = min(ranges)
    self.max_x = max(ranges)
    hit = True
    v = -10
    hits = []
    #while hit:
    for i in range(200):
      h = (v * (v+1)) / 2
      y1 = abs(self.yrange[0] - h)
      y2 = abs(self.yrange[1] - h)
      maxy = max([y1,y2])
      miny = min([y1,y2])
      #print 'Y Offset Target @', h, miny, maxy
      yv = 1
      vh = (yv * (yv + 1)) / 2
      hit = False
      while vh <= maxy:
        if vh >= miny:
          #print 'Hits at fall from ', h
          hits.append((h,v))
          hit = True
          break;
        yv += 1
        vh = (yv * (yv + 1)) / 2
      v += 1
    #print hits
    highest = hits[len(hits)-1]
    self.max_y = highest[1]
    self.max_height = highest[0]
    #print highest

  def simulate(self):
    minx = self.min_x
    maxx = self.xrange[1]
    miny = self.yrange[0]
    maxy = self.max_y
    print 'Simulation', minx, miny, '->', maxx, maxy
    for y in range(miny, maxy+1):
      for x in range(minx, maxx+1):
        if self.hits(x, y):
          #print (x, y)
          self.options.append((x,y))

  def hits(self, vx, vy):
    x = 0
    y = 0
    while x <= self.xrange[1] and y >= self.yrange[0]:
      if x >= self.xrange[0] and y <= self.yrange[1]:
        #print (x, y), 'in ', self.xrange, self.yrange
        return True
      x += vx
      y += vy
      if vx > 0:
        vx -= 1
      vy -= 1
    return False
    

  def result(self):
    #target area: x=206..250, y=-105..-57
    self.define([206, 250], [-105, -57])
    self.simulate()
    print self.options
    print len(self.options)
    #print 'Max Height:', self.max_height

if __name__ == '__main__':
  puz = Puzzle()
  puz.result()

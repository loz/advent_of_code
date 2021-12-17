class Puzzle:
  
  def define(self, xrange, yrange):
    self.xrange = xrange
    self.yrange = yrange
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
    v = 1
    hits = []
    #while hit:
    for i in range(10000):
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
    print hits
    highest = hits[len(hits)-1]
    #print highest
    self.max_y = highest[1]
    self.max_height = highest[0]

  def result(self):
    #target area: x=206..250, y=-105..-57
    self.define([206, 250], [-105, -57])
    print 'Max Height:', self.max_height

if __name__ == '__main__':
  puz = Puzzle()
  puz.result()

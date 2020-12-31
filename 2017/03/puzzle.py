import math

class Puzzle:

  def loc(self, val):
    if val == 2:
      return (1,0)
    isqrt = int(math.floor(math.sqrt(val)))
    lsqr = isqrt*isqrt
    nsqr = (isqrt+1)*(isqrt+1)
    rem = val - lsqr
    if isqrt % 2 == 0:
      if rem == 0:
        xy = isqrt / 2
        return (1-xy, 0 - xy)
      side = isqrt+1
      mins = (-1*(side/2))
      maxs = (side/2)
      #print 'EEVal:', val, '=', lsqr,'..', 'n', nsqr, 'side:', side, (-1*(side/2)), '..', ((side/2))
      if val <= lsqr + side:
        #print 'left', rem
        return (mins, mins + rem - 1)
      else:
        #print 'bottom', rem - side
        rem = rem - side
        return (mins + rem, maxs)
    else:
      if rem == 0:
        xy = (isqrt-1) / 2
        return (xy, xy)
      side = isqrt+1
      mins = (-1*(side/2))
      maxs = (side/2)
      #print 'OOVal:', val, '=', lsqr,'..', 'n', nsqr, 'side:', side, (-1*(side/2)), '..', ((side/2))
      #print rem
      if val <= lsqr + side:
        #print 'right', rem
        return (maxs, maxs - rem)
      else:
        #print 'top', rem - side
        rem = rem - side
        return (maxs - rem, mins)
    return (-99, -99)

  def dump(self, size):
    print 'Size', size
    grid = {}
    for i in range(1, (size*size)+1):
      x, y = self.loc(i)
      grid[(x,y)] = i
    
    mins = -1 * (size/2)
    maxs = size/2
    print mins, maxs
    for y in range(mins, maxs+1):
      for x in range(mins, maxs+1):
        print "%3d" % grid[(x,y)],
      print ''
  
  def result(self):
    self.dump(31)
    x, y = self.loc(1024)
    print 1024, x, y , '=', abs(x)+abs(y)
    x, y = self.loc(265149)
    print 265149, x, y , '=', abs(x)+abs(y)

if __name__ == '__main__':
  puz = Puzzle()
  puz.result()

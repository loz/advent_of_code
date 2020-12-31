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

  def gen1(self, size):
    print 'Size', size
    grid = {}
    for i in range(1, (size*size)+1):
      x, y = self.loc(i)
      grid[(x,y)] = i
    return grid

  def gen2(self, size, upper):
    grid = {(0,0): 1}
    found = False
    for i in range(2, (size*size) + 1):
      x, y = self.loc(i)
      val = self.nsum(x, y, grid)
      if val > upper and not found:
        print 'LARGE', val
        found = True
      grid[(x, y)] = val
    return grid

  def nsum(self, x, y, grid):
    total = 0
    deltas = [(-1,-1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dxdy in deltas:
      dx, dy = dxdy
      total += grid.get((x+dx, y+dy), 0)
    return total

  def dump(self, size, grid):
    mins = -1 * (size/2)
    maxs = size/2
    #print mins, maxs
    for y in range(mins, maxs+1):
      for x in range(mins, maxs+1):
        print "%8d" % grid[(x,y)],
      print ''
  
  def result(self):
    grid = self.gen2(9, 265149)
    self.dump(9, grid)

if __name__ == '__main__':
  puz = Puzzle()
  puz.result()

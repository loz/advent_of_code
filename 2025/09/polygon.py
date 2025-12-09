
def ordered(ax, ay, bx, by):
  minx = min(ax, bx)
  maxx = max(ax, bx)
  miny = min(ay, by)
  maxy = max(ay, by)
  return (minx, miny, maxx, maxy)

def clip_axis(bounds, a, b):
  na = a
  nb = b
  if a < bounds[0]:
    if b > bounds[1]:
      #print('clip left/right')
      na = bounds[0]
      nb = bounds[1]
    elif b < bounds[0]:
      na = bounds[0]
      nb = bounds[0]
    else:
      #print ('clip left')
      na = bounds[0]
  elif a > bounds[1]:
    na = bounds[1]
    nb = bounds[1]
  else: #a in bounds
    if b < bounds[1]:
      pass
      #print('start/end inside')
    else: #by > end
      #print('start in, end out')
      nb = bounds[1]
  return (na, nb)

def filter_edges(points, w, h, corners):
  filtered = []
  for point in points:
    x, y = point
    #print(x,y, 'vs', corners, x in w, y in h)
    if x in w or y in h:
      if (x,y) in corners:
        filtered.append(point)
    else:
      filtered.append(point)
  return filtered

def clip_polygon(rect, coords):
  aset = coords[0:-1]
  bset = coords[1:]
  lines = zip(aset, bset)
  w, h = rect
  corners = [(w[0], h[0]), (w[1], h[0]), (w[0], h[1]), (w[1], h[1])]
  clipped = set()
  for line in lines:
    a, b = line
    ax, ay = a
    bx, by = b
    
    ax, ay, bx, by = ordered(ax, ay, bx, by)
    nay, nby = clip_axis(h, ay, by)
    nax, nbx = clip_axis(w, ax, bx)

    #print(ax, ay, '->', bx, by, 'vs', rect, '=>', nax, nay, '->', nbx, nby)
    clipped.add((nax, nay))
    clipped.add((nbx, nby))
  clipped = filter_edges(clipped, w, h, corners)
  return list(clipped)

def line_cuts(s,e, bound):
  bs, be = bound
  if s <= bs and e >= be:
    return True
  elif s > bs and s < be:
    if e >= be:
      return True
  return False

def polygon_cuts_rect(rect, coords):
  aset = coords[0:-1]
  bset = coords[1:]
  lines = zip(aset, bset)
  vertz = []
  horiz = []
  w, h = rect
  for line in lines:
    a, b = line
    ax, ay = a
    bx, by = b
    if ax == bx:
      vertz.append(line)
    else:
      horiz.append(line)
  #print(vertz)
  #print(horiz)
  for line in vertz:
    a, b = line
    ax, ay = a
    bx, by = b
    #print('V:', ay, by, rect)
    if ax > w[0] and ax < w[1]:
      #print('In Hbound')
      if line_cuts(ay,by, h):
        return True
  for line in horiz:
    a, b = line
    ax, ay = a
    bx, by = b
    #print('V:', ay, by, rect)
    if ay > h[0] and ay < h[1]:
      #print('In Hbound')
      if line_cuts(ax,bx, w):
        return True
  return False

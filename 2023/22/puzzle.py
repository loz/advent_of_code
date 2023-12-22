import sys

class Puzzle:

  def process(self, text):
    self.cubes = []
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      lhs, rhs = line.split('~')
      lhs = self.process_coord(lhs)
      rhs = self.process_coord(rhs)
      self.cubes.append( (lhs, rhs) )

  def process_coord(self, txt):
    vals = txt.split(',')
    vs = [int(v) for v in vals]
    return (vs[0], vs[1], vs[2])

  def fall(self, cubes):
    ncubes = list(cubes)

    didFall = True
    fallcount = 0
    #ASSERT: Because we re falling bottom UP, each block only falls ONCE
    fallen = []
    while(didFall):
      #if fallcount > 5:
      #  break
      didFall = False
      bottoms, tops = self.rescan(ncubes)
      #print("="*80)
      #print(ncubes)
      #print('Bottoms')
      #print(bottoms)
      #print('Tops')
      #print(tops)

      for cube in bottoms:
        z, id, *_ = cube
        if id not in fallen: #already fell
          #print('Falling: #'+str(id), 'from', z)
          below = [c for c in tops if self.isover(cube, c)]
          if below:
            c = below[0]
            nz = c[0]+1
            if z == nz:
              #print('Supported')
              pass
            else:
              #print('Fall To', nz, 'from', z)
              dz = nz-z
              p1, p2 = cubes[id]
              ncube = ( (p1[0], p1[1], p1[2] + dz), (p2[0], p2[1], p2[2]+dz) )
              ncubes[id] = ncube
              #print('->', ncube)
              didFall = True
              fallen.append(id)
              fallcount += 1
              break
          else:
            if z > 1:
              #Fall to ground
              #print('Fall To Ground')
              nz = 1
              dz = nz-z
              p1, p2 = cubes[id]
              ncube = ( (p1[0], p1[1], p1[2] + dz), (p2[0], p2[1], p2[2]+dz) )
              ncubes[id] = ncube
              #print((p1,p2), '->', ncube)
              didFall = True
              fallcount += 1
              fallen.append(id)
              break
            else:
              #print('On Ground')
              pass

    return ncubes, fallcount

  def anyfall(self, cubes):
    didFall = False
    bottoms, tops = self.rescan(cubes)
    for cube in bottoms:
      z, id, *_ = cube
      below = [c for c in tops if self.isover(cube, c)]
      if below:
        c = below[0]
        nz = c[0]+1
        if z == nz:
          #print('Supported')
          pass
        else:
          return True
      else:
        if z > 1:
          return True
        else:
          #print('On Ground')
          pass

    return False

  def buildtree(self, cubes):
    bottoms, tops = self.rescan(cubes)
    supporters = {}
    for cube in bottoms:
      z, id, *_ = cube
      if id not in supporters:
        supporters[id] = []
      below = [c for c in tops if self.isover(cube, c)]
      if below:
        for c in below:
          nz = c[0]+1
          if z == nz:
            supporters[id].append(c[1])
      else:
        if z == 1:
          supporters[id].append(-1)
    return supporters

  def inverttree(self, tree):
    #Swap CUBE -> [SUPPORTED BY]
    # to  CUBE -> [SUPPORTS]
    newtree = {}
    for k in tree:
      ss = tree[k]
      for c in ss:
        if c not in newtree:
          newtree[c] = []
        if k not in newtree: #May only be k and support NONE
          newtree[k] = []
        newtree[c].append(k)
    return newtree

  def rescan(self, cubes):
    #Bottoms of all cubes 
    #Tops of all cubes
    bottoms = []
    tops = []
    for id, cube in enumerate(cubes):
      (x1,y1,z1), (x2,y2,z2) = cube
      b = (z1, id, (x1,y1), (x2,y2))
      t = (z2, id, (x1,y1), (x2,y2))
      bottoms.append(b)
      tops.append(t)
    #sort them
    bottoms = sorted(bottoms)
    tops = sorted(tops, reverse=True)
    return bottoms, tops

  def isover(self, cubea, cubeb):
    za = cubea[0]
    zb = cubeb[0]
    if zb < za:
      #possible
      (ax1, ay1), (ax2, ay2) = cubea[2], cubea[3]
      (bx1, by1), (bx2, by2) = cubeb[2], cubeb[3]
      #c1 = ax1 <= bx2
      #c2 = ax2 >= bx1
      #c3 = ay1 <= by2
      #c4 = ay2 >= by1
      #return c1 and c2 and c3 and c4
      return (ax1 <= bx2) and (ax2 >= bx1) and (ay1 <= by2) and (ay2 >= by1)
    else:
      return False

  def traverse_impact(self, id, supporters, supporting):
    tovisit = [id]
    fallen = [id]
    while(tovisit):
      fid = tovisit.pop(0)
      effected = supporting[fid]
      #print('Fallen', fid, 'hits', effected, '(', fallen, ')')
      for c in effected:
        needs = supporters[c]
        has = [n for n in needs if n not in fallen]
        #print(c, 'N->', needs, 'has', has)
        if has == [] and c not in fallen:
          fallen.append(c)
          tovisit.append(c)
      #print('-'*20)
    return fallen 


  def result(self):
    self.result2()

  def result1(self):
    print('Settline Bricks')
    settled, _ = self.fall(self.cubes)
    print('Scanning')
    safe = []
    for n, brick in enumerate(settled):
      others = [b for b in settled if b != brick]
      willfall = self.anyfall(others)
      if not willfall:
        safe.append(brick)
      print(n, '->', willfall)
    print('Total Safe', len(safe))

  def result2(self):
    print('Settline Bricks')
    settled, _ = self.fall(self.cubes)
    print('Building Tree')
    supporters = self.buildtree(settled)
    supporting = self.inverttree(supporters)

    #for k in supporting:
    #  print(k, supporting[k])

    print('Scanning')
    total = 0
    for n, brick in enumerate(settled):
      impacted = self.traverse_impact(n, supporters, supporting)
      total += (len(impacted)-1) #-1 as the removed brick is in the list
      print(n, '->', supporting[n], len(impacted))
    print('Total Falls', total)


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

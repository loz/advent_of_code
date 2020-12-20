import math

class Puzzle:

  def process(self, text):
    lines = text.split('\n')
    self.tiles = {}
    while len(lines) > 0:
      line = lines.pop(0)
      if line.startswith('Tile'):
        id = line.replace('Tile ', '').replace(':','')
        id = int(id)
        tile, lines = self.parse_tile(lines)
        self.tiles[id] = tile
    self.identify_edges()
    matchtable = {}
    for tileid in self.tiles:
      matches = self.matches(tileid)
      matchtable[tileid] = matches
    self.matchtable = matchtable

  def identify_edges(self):
    self.edges = {}
    for id in self.tiles:
      self.edges[id] = self.tile_edges(self.tiles[id])

  def tile_edges(self, tile):
    rows = filter(lambda r: r.strip() != '', tile.split('\n'))
    width = len(rows[0])
    left = ''.join(map(lambda r: r[0], rows))
    right = ''.join(map(lambda r: r[width-1], rows))
    return [
      rows[0],
      left,
      right,
      rows[len(rows)-1]
    ]

  def matches(self, id):
    edges = self.edges[id]
    matches = [
      [], [], [], []
    ]
    for tileid in self.edges:
      if tileid != id: #skip self
        tedges = self.edges[tileid]
        for eid in range(4):
          edge = tedges[eid]
          redge = edge[::-1]
          if edge in edges:
            matchid = edges.index(edge)
            matches[matchid].append((tileid, eid))
          elif redge in edges:
            matchid = edges.index(redge)
            matches[matchid].append((tileid, eid))
    return matches
 
  def parse_tile(self, lines):
    tile = ""
    while len(lines) > 0:
      line = lines.pop(0)
      if line.strip() == '':
        return tile , lines
      tile += line + '\n'
    return tile, lines
  
  def neighbours(self, x, y, sequence, dim):
    deltas = [
      (-1, 0), (1, 0), (0, -1), (0, 1)
    ]
    locs = map(lambda d: (x + d[0], y + d[1]), deltas)
    locs = filter(lambda l: l[0] >= 0 and l[1] >= 0, locs)
    locs = filter(lambda l: l[0] < dim and l[1] < dim, locs)
    return map(lambda l: (l, sequence[l[1]][l[0]]), locs)

  def neighbour(self, delta, x, y, sequence, dim):
    dx = x + delta[0]
    dy = y + delta[1]
    if dx >= 0 and dy >= 0 and dx < dim and dy < dim:
      return sequence[dy][dx]
    else:
      return None

  def connections(self, matches):
    edges = []
    for match in matches:
      for edge in match:
        edges.append(edge[0])
    return edges

  def find_orientation(self, id, x, y, sequence, dim):
    tile = self.tiles[id]
    matches = self.matchtable[id]
    north = self.neighbour((0,-1), x, y, sequence, dim)
    south = self.neighbour((0, 1), x, y, sequence, dim)
    east =  self.neighbour((-1,0), x, y, sequence, dim)
    west =  self.neighbour(( 1,0), x, y, sequence, dim)
    ns = [north, south, east, west]
    borders = []
    for match in matches:
      if match == []:
        borders.append(None)
      else:
        tiles = map(lambda b: b[0], match)
        for btile in tiles:
          if btile in ns:
            borders.append(btile)
    top, left, right, bottom = borders
    #print 'id', id,
    #print 'matches', matches
    #print 'edges', top, bottom, left, right
    #print 'neighbours', north, south, east, west
    target = [north, south, east, west]
    if [top, bottom, left, right]  == target: #Correct orientation
      return tile
    #print 'Flip or Rotate'
    if [top, bottom, right, left] == target: #H Mirror
      return self.hmirror(tile)

    if [bottom, top, left, right] == target: #V Mirror
      return self.vmirror(tile)

    if [bottom, top, right, left] == target: #HV Mirror
      return self.hmirror(self.vmirror(tile))

    #print 'Must be rotated verion'
    tile = self.rotate(tile)
    if [left, right, top, bottom] == target: #90
      return tile
    if [left, right, bottom, top] == target: #90 H Mirror
      return self.hmirror(tile)
    if [right, left, top, bottom] == target: #90 V Mirror
      return self.vmirror(tile)
    if [right, left, bottom, top] == target: #90 HV Mirror
      return self.hmirror(self.vmirror(tile))
    return '?????????\n' * 9

  def assemble_map(self):
    sequence = self.find_sequence()
    dim = len(sequence[0])
    tiles = []
    for y in range(dim):
      row = []
      for x in range(dim):
        id = sequence[y][x]
        tile = self.find_orientation(id, x, y, sequence, dim)
        row.append(tile)
      tiles.append(row)
    print '====== TILES ====='
    for row in tiles:
      print row

    return """ABC
DEF
GHI
"""

  def find_sequence(self):
    dim = int(math.sqrt(len(self.tiles)))
    print dim, 'x', dim
    corners = []
    sequence = []
    matchtable = self.matchtable
    for i in range(dim):
      sequence.append([None] * dim)
    for tileid in self.tiles:
      numedges = len(filter(lambda m: m == [], matchtable[tileid]))
      if numedges == 2:
        corners.append(tileid)
    #FIND Top CORNER SLOTS

    tops = filter(lambda c: matchtable[c][0] == [], corners)
    tls= filter(lambda c: matchtable[c][1] == [], tops)
    topleft = tls[0]
    sequence[0][0] = topleft
    placed = [topleft]
    edges = [(0,0,topleft)]
    while len(edges) > 0:
      newedges = []
      for edge in edges:
        #print edge
        x, y, tile = edge
        neighbours = self.neighbours(x, y, sequence, dim)
        missing = filter(lambda n: n[1] == None, neighbours)
        #print 'Find', missing
        options = self.connections(matchtable[tile])
        #print 'Options', options, placed
        #Filter out already placed items
        options = filter(lambda o: o not in placed, options)
        #print 'Available Options', options
        conditions = []
        for mtile in missing:
          mloc, _ = mtile
          mx, my = mloc
          neighbours = self.neighbours(mx, my, sequence, dim)
          constraints = filter(lambda n: n[1] != None, neighbours)
          constraints = map(lambda c: c[1], constraints)
          conditions.append((mloc, constraints))
        #Sort to deal with most constrained first
        conditions.sort(key=lambda c: len(c[1]), reverse=True)
        
        for condition in conditions:
          mloc, constraints = condition
          mx, my = mloc

        #for mtile in missing:
          #mloc, _ = mtile
          #mx, my = mloc
          #neighbours = self.neighbours(mx, my, sequence, dim)
          #constraints = filter(lambda n: n[1] != None, neighbours)
          #constraints = map(lambda c: c[1], constraints)
          #print mx, my, 'must connect to', constraints
          valid = []
          for option in options:
            oedges = self.connections(matchtable[option])
            included = set(oedges) & set(constraints)
            #print option, oedges, included
            if included == set(constraints):
              valid.append(option)
          #print 'Valid', valid
          #Pick first as any is apropriate
          chosen = valid[0]
          sequence[my][mx] = chosen
          placed.append(chosen)
          newedges.append((mx, my, chosen))
          options.remove(chosen)
          #print 'Remain', options
        #for mtile in tiles:
        #  print mtile, matchtable[mtile]
      edges = newedges
      #self.print_sequence(sequence)
    
    self.print_sequence(sequence)
    return sequence

  def print_sequence(self, sequence):
    print '==== SEQUENCE ===='
    for row in sequence:
      print row
    

  def hmirror(self, img):
    mirror = ''
    rows = filter(lambda r: r.strip() != '', img.split('\n'))
    for row in rows:
      mirror = mirror + row[::-1] + '\n'
    return mirror

  def vmirror(self, img):
    mirror = ''
    rows = filter(lambda r: r.strip() != '', img.split('\n'))
    rows.reverse()
    for row in rows:
      mirror = mirror + row + '\n'
    return mirror

  def rotate(self, img):
    rotated = ''
    rows = filter(lambda r: r.strip() != '', img.split('\n'))
    width = len(rows[0])
    height = len(rows)
    for x in range(width):
      row = ''
      for y in range(height):
        row += rows[y][x]
      rotated += row + '\n'
    return rotated
    
  def result1(self):
    corners = []
    for tileid in self.tiles:
      matches = self.matches(tileid)
      numedges = len(filter(lambda m: m == [], matches))
      if numedges == 2:
        corners.append(tileid)
      #print tileid, self.edges[tileid], matches
    cmult = 1
    for corner in corners:
      cmult *= corner
    print 'Corners', corners, cmult

  def result(self):
    puz.assemble_map()


if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result1()
  puz.result()

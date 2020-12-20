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
    
  def result(self):
    corners = []
    for tileid in self.tiles:
      matches = self.matches(tileid)
      numedges = len(filter(lambda m: m == [], matches))
      if numedges == 2:
        corners.append(tileid)
      print tileid, self.edges[tileid], matches
    cmult = 1
    for corner in corners:
      cmult *= corner
    print 'Corners', corners, cmult

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

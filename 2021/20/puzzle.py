class Puzzle:

  def process(self, text):
    self.algorithm = []
    lines = text.split('\n')
    self.parse_algorithm(lines[0])
    lines = lines[2:]
    self.parse_map(lines)

  def parse_map(self, lines):
    rows = []
    self.infinite = '.'
    for line in lines:
      if len(line) > 0:
        row = [ch for ch in line]
        rows.append(row)
    self.map = rows
    self.height = len(rows)
    self.width = len(rows[0])

  def get_bit(self, x, y):
    if x < 0 or y < 0 or x >= self.width or y >= self.height:
      return self.infinite
    else:
      return self.map[y][x]
  
  def get_matrix(self, x, y):
    return self.get_bit(x-1, y-1) + \
      self.get_bit(x, y-1) + \
      self.get_bit(x+1, y-1) + \
      self.get_bit(x-1, y) + \
      self.get_bit(x, y) + \
      self.get_bit(x+1, y) + \
      self.get_bit(x-1, y+1) + \
      self.get_bit(x, y+1) + \
      self.get_bit(x+1, y+1)

  def enhance(self, x, y):
    matrix = self.get_matrix(x,y)
    #print (x, y), matrix
    matrix = matrix.replace('.', '0')
    matrix = matrix.replace('#', '1')
    value = int(matrix, 2)
    return self.algorithm[value]

  def parse_algorithm(self, line):
    self.algorithm = [ch for ch in line]
  
  def enhance_image(self):
    newmap = []
    for y in range(self.height + 4):
      row = []
      oy = y - 2
      for x in range(self.width + 4):
        ox = x - 2
        row.append(self.enhance(ox,oy))
      newmap.append(row)
    self.map = newmap
    self.width += 4
    self.height += 4
    #Infinity changes
    if self.infinite == '#':
      self.infinite=self.algorithm[511]
    else:
      self.infinite=self.algorithm[0]

  def tostring(self):
    text = ''
    for row in self.map:
      text += ''.join(row) + '\n'
    return text

  def result(self):
    for i in range(50):
      self.enhance_image()
    print self.tostring()
    count = 0
    for row in self.map:
      for bit in row:
        if bit == '#':
          count += 1
    print 'Count', count

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

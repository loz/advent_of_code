import sys

class Puzzle:
  def __init__(self):
    self.state = ".#.\n..#\n###"
    self.patterns = {}

  def process(self, text):
    for line in text.split('\n'):
      self.process_line(line)

  def image(self):
    return self.state

  def enhanceImage(self):
    parts = self.fragment()
    newimg = []
    for row in parts:
      nrows = []
      for col in row:
        ncol = self.enhance(col)
        nrows.append(ncol.split('\n'))
      newimg.append(self.combine(nrows))
    self.state = "\n".join(newimg)

  def combine(self, chunks):
    linecount = len(chunks[0])
    joined = []
    for l in range(linecount):
      line = ""
      for chunk in chunks:
        line += chunk[l]
      joined.append(line)
    return "\n".join(joined)

  def fragment(self):
    lines = self.state.split('\n')
    if len(lines) % 2 == 0:
      return self.fragment2(lines)
    else:
      return self.fragment3(lines)

  def fragment2(self, lines):
    parts = []
    size = len(lines)
    for y in range(0,size,2):
      tline = lines[y]
      bline = lines[y+1]
      row = []
      for x in range(0,size,2):
        #print (x,y), (x+1, y+1)
        sq = tline[x] + tline[x+1] + '\n' + bline[x] + bline[x+1] 
        row.append(sq)
      parts.append(row)
    return parts

  def fragment3(self, lines):
    parts = []
    size = len(lines)
    for y in range(0,size,3):
      tline = lines[y]
      mline = lines[y+1]
      bline = lines[y+2]
      row = []
      for x in range(0,size,3):
        sq = tline[x] + tline[x+1] + tline[x+2] + '\n' \
           + mline[x] + mline[x+1] + mline[x+2] + '\n' \
           + bline[x] + bline[x+1] + bline[x+2]
        row.append(sq)
      parts.append(row)
    return parts

  def process_line(self, line):
    if line != '':
      left, right = line.split(' => ')
      key = left.replace('/', '\n')
      value = right.replace('/', '\n')
      self.patterns[key] = value

  def enhance(self, chunk):
    if chunk in self.patterns.keys():
      return self.patterns[chunk]
    
    rotated = chunk
    for times in range(3):
      rotated = self.rotate(rotated)
      if rotated in self.patterns.keys():
        return self.patterns[rotated]

    rotated = self.hflip(chunk)
    if rotated in self.patterns.keys():
      return self.patterns[rotated]

    for times in range(3):
      rotated = self.rotate(rotated)
      if rotated in self.patterns.keys():
        return self.patterns[rotated]

    return '??'

  def hflip(self, chunk):
    #ASSERT only 3x3 can flip, as rotate already works for 2x2
    parts = [ch for ch in chunk]
    #abc/def/ghi => cba/fed/ihg
    #0123456789T
    return parts[2] + parts[1] + parts[0] + '\n' + parts[6] + parts[5] + parts[4] + '\n' + parts[10] + parts[9] + parts[8]

  def vflip(self, chunk):
    #ASSERT only 3x3 can flip, as rotate already works for 2x2
    parts = [ch for ch in chunk]
    #abc/def/ghi => ghi/def/abc
    #0123456789T
    return parts[8] + parts[9] + parts[10] + '\n' + parts[4] + parts[5] + parts[6] + '\n' + parts[0] + parts[1] + parts[2]

  def rotate(self, chunk):
    #Chunks are 2x2 or 3x3
    parts = [ch for ch in chunk]
    if len(parts) == 5: #2x2
      #ab/cd => ca/db
      #01234
      return parts[3] + parts[0] + '\n' + parts[4] + parts[1] 
    else:
      #abc/def/ghi => gda/heb/ifc
      #0123456789T
      return parts[8] + parts[4] + parts[0] + '\n' + parts[9] + parts[5] + parts[1] + '\n' + parts[10] + parts[6] + parts[2]

  def result(self):
    print self.state
    for i in range(18):
      print i+1, '-'*10
      self.enhanceImage()
      print self.state
      print self.state.count('#'), 'Lights On'



if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

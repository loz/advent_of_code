class Puzzle:

  def process(self, text):
    self.marker = -1
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    markersize = 14
    pos = 0
    buff = []
    if line != '':
      for ch in line:
        if len(buff) == markersize:
          buff = buff[1:markersize]
        buff.append(ch)
        pos += 1
        print pos, buff, len(set(buff))
        if len(set(buff)) == markersize:
          self.marker = pos
          return

  def result(self):
    print 'Marker', self.marker



if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

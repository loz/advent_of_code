import sys

class Puzzle:

  def process(self, text):
    self.chunks = []
    self.boxes = []
    for b in range(256):
      self.boxes.append([])
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      chunks = line.split(',')
      for ch in chunks:
        if ch != '':
          self.chunks.append(ch)

  def execute(self, action):
    if '=' in action:
      label, rhs = action.split('=')
      val = int(rhs)
      bid = self.hash(label)
      idx = None
      for i, v in enumerate(self.boxes[bid]):
        if (v[0] == label):
          idx = i
          break
      if idx != None:
        self.boxes[bid][idx] = (label, val)
      else:
        self.boxes[bid].append((label, val))
    elif '-' in action:
      label = action.replace('-','')
      bid = self.hash(label)
      newset = []
      for b in self.boxes[bid]:
        if b[0] != label:
          newset.append(b)
      self.boxes[bid] = newset


  def focus(self, num, items):
    n = 0
    for i, v in enumerate(items):
      #print(num, i+1, v[1])
      n += num * (i+1) * v[1]
    return n

  def hash(self, text):
    val = 0
    for ch in text:
      o = ord(ch)
      #print(val, ch, o)
      val = ((val + o)*17) % 256
    return val

  def result(self):
   self.result2()

  def result2(self):
    for ch in self.chunks:
      self.execute(ch)

    total = 0
    for i, b in enumerate(self.boxes):
      f = self.focus(i+1, b)
      total += f
      print(b, f)
    print('Total', total)


  def result1(self):
    total = 0
    for ch in self.chunks:
      v = self.hash(ch)
      print(ch, ' ->', v)
      total += v
    print('Total', total)


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

class SnailInt:
  def __init__(self, val):
    self.literal = True
    self.val = val
  
  def add_on_left(self, num):
    self.val += num.val

  def add_on_right(self, num):
    self.add_on_left(num)

  def string(self):
    return str(self.val)

class SnailfishNumber:
  def __init__(self):
    self.literal = False
    self.parent = None

  def parse(self, chars):
    token, chars = self.pull(chars)
    if token != '[':
      raise 'Missing ['

    if chars[0] == '[': #child
      child = SnailfishNumber()
      chars = child.parse(chars)
      child.parent = self
      self.left = child
    else:
      token, chars = self.pull(chars)
      self.left = SnailInt(int(token))

    token, chars = self.pull(chars)
    if token != ',':
      raise 'Missing ,'

    if chars[0] == '[': #child
      child = SnailfishNumber()
      child.parent = self
      chars = child.parse(chars)
      self.right = child
    else:
      token, chars = self.pull(chars)
      self.right = SnailInt(int(token))

    token, chars = self.pull(chars)
    if token != ']':
      raise 'Missing ]'

    #What is left is from outside number
    return chars

  def pull(self, chars):
    ch = chars[0]
    chars = chars[1:]
    #print ch, ':', ''.join(chars)
    return ch, chars

  def string(self):
    return "(L= " + self.left.string() + ', R=' + self.right.string() + ')'

  def reduce(self):
    exploded = self._explode(0)
    print self.string()

  def leftmost_add(self, num, target):
    #print 'L-Add', num.string(), target.string()
    if self.right == target:
      self.left.add_on_right(num)
    elif self.parent:
      self.parent.leftmost_add(num, self)

  def rightmost_add(self, num, target):
    #print 'R-Add', num.string(), target.string()
    if self.left == target:
      self.right.add_on_left(num)
    elif self.parent:
      self.parent.rightmost_add(num, self)

  def add_on_left(self, num):
    self.left.add_on_left(num)

  def add_on_right(self, num):
    self.right.add_on_right(num)

  def _explode(self, depth):
    if depth == 4:
      #print 'At 4', self.string()
      return True
    if not self.left.literal:
      if self.left._explode(depth + 1):
        if depth == 3:
          #print 'Explode', self.left.string()
          vleft = self.left.left
          vright = self.left.right
          self.rightmost_add(vright, self.left)
          self.leftmost_add(vleft, self.left)
          self.left = SnailInt(0)
        return True
  
    if not self.right.literal:
      if self.right._explode(depth + 1):
        if depth == 3:
          #print 'Explode R', self.right.string()
          vleft = self.right.left
          vright = self.right.right
          self.rightmost_add(vright, self.right)
          self.leftmost_add(vleft, self.right)
          self.right = SnailInt(0)
        return True

    #No explosion
    return False
   

class Puzzle:

  def process(self, text):
    self.numbers = []
    lines = text.split('\n')
    for line in lines:
      self.process_line(line)

  def process_line(self, line):
      if len(line) == 0:
        return
      line = line.strip()
      line = [ch for ch in line]
      number = SnailfishNumber()
      number.parse(line)
      self.numbers.append(number)

  def result(self):
    pass

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

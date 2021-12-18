import math

class SnailInt:
  def __init__(self, val):
    self.literal = True
    self.val = val

  def magnitude(self):
    return self.val

  def _split(self):
    if self.val >= 10:
      #print 'SPLIT HIT', self.val
      newnum = SnailfishNumber()
      left = int(math.floor(self.val / 2.0))
      right = int(math.ceil(self.val / 2.0))
      newnum.setleft(SnailInt(left))
      newnum.setright(SnailInt(right))
      #print 'Split', self.val, 'to', newnum.string()
      self.parent.replace_child(self, newnum)
      return True
    else:
      return False

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

  def add(self, other):
    num = SnailfishNumber()
    num.setleft(self)
    num.setright(other)
    num.reduce()
    return num

  def magnitude(self):
    return 3 * self.left.magnitude() + 2 * self.right.magnitude()

  def setleft(self, child):
    child.parent = self
    self.left = child

  def setright(self, child):
    child.parent = self
    self.right = child

  def replace_child(self, child, newchild):
    if self.left == child:
      self.setleft(newchild)
    elif self.right == child:
      self.setright(newchild)
    else:
      raise 'Not Child!'

  def parse(self, chars):
    token, chars = self.pull(chars)
    if token != '[':
      raise 'Missing ['

    if chars[0] == '[': #child
      child = SnailfishNumber()
      chars = child.parse(chars)
      self.setleft(child)
    else:
      token, chars = self.pull(chars)
      self.setleft(SnailInt(int(token)))

    token, chars = self.pull(chars)
    if token != ',':
      raise 'Missing ,'

    if chars[0] == '[': #child
      child = SnailfishNumber()
      chars = child.parse(chars)
      self.setright(child)
    else:
      token, chars = self.pull(chars)
      self.setright(SnailInt(int(token)))

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
    while True:
      #print '>>', self.string()
      if self._explode(0):
        next
      else:
        if self._split():
          next
        else:
          return False

  def _split(self):
    #print 'Split', self.string()
    if not self.left._split():
      return self.right._split()
    else:
      return True

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
          self.setleft(SnailInt(0))
        return True
  
    if not self.right.literal:
      if self.right._explode(depth + 1):
        if depth == 3:
          #print 'Explode R', self.right.string()
          vleft = self.right.left
          vright = self.right.right
          self.rightmost_add(vright, self.right)
          self.leftmost_add(vleft, self.right)
          self.setright(SnailInt(0))
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
    value = self.numbers[0]
    cur = 1
    while cur < len(self.numbers):
      value = value.add(self.numbers[cur])
      cur += 1
    print 'Final Value', value.string()
    print 'Magnitude', value.magnitude()

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

import sys

class List:
  def __init__(self, num):
    self.num = num
    self.left = None
    self.right = None
    self.ishead = False

  def nth(self, n):
    cursor = self
    while n > 0:
      n-=1
      cursor = cursor.right

    return cursor

  def find_head(self):
    if self.ishead:
      return self
    else:
      return self.right.find_head()

  def move_left(self, count):
    if count == 0:
      return

    cursor = self
    if cursor.ishead: #Move Head
      cursor.left.ishead = True
      cursor.ishead = False
    while count > 0:
      #  Ll L [*] R Rr
      #  NL=Ll, NR=L
      newleft = cursor.left.left
      newright = cursor.left
      #print newleft.num, newright.num
      # L->R, L<-R
      cursor.right.left = newright
      newright.right = cursor.right

      # Ll->[*], [*]<-L
      newleft.right = cursor
      newright.left = cursor
      # R<-[*], [*]->Rr
      cursor.left = newleft
      cursor.right = newright
      # * L R [*] Rr
      #print cursor.left.num, cursor.num, cursor.right.num
      count -= 1
  def move_right(self, count):
    if count == 0:
      return

    cursor = self
    if cursor.ishead: #Move Head
      cursor.right.ishead = True
      cursor.ishead = False
    while count > 0:
      #  * L [*] R Rr
      #  NL=R, NR=Rr
      newleft = cursor.right
      newright = cursor.right.right
      #print newleft.num, newright.num
      # L->R, L<-R
      cursor.left.right = newleft
      newleft.left = cursor.left
      # R->[*], [*]<-Rr
      newleft.right = cursor
      newright.left = cursor
      # R<-[*], [*]->Rr
      cursor.left = newleft
      cursor.right = newright
      # * L R [*] Rr
      #print cursor.left.num, cursor.num, cursor.right.num
      count -= 1
      

  def to_a(self):
    cursor = self.right
    arr = [self.num]
    while cursor != self:
      arr.append(cursor.num)
      cursor = cursor.right
    return arr

  def atindex(self, idx):
    if idx == 0:
      return self
    else:
      return self.right.atindex(idx-1)

  def find(self, val, term = None):
    if self.num == val:
      return self
    cursor = self.right
    while cursor != self:
      if cursor.num == val:
        return cursor
      cursor = cursor.right
    return None

class Puzzle:

  def process(self, text):
    self.order = []
    self.head = None
    self.last = None
    for line in text.split('\n'):
      self.process_line(line)
    #Make Circular
    self.last.right = self.head
    self.head.left = self.last

  def process_line(self, line):
    if line != '':
      val = List(int(line))
      self.order.append(val)
      if self.last != None:
        self.last.right = val
        val.left = self.last
      else:
        val.ishead = True
        self.head = val
      self.last = val

  def atindex(self, idx):
    return self.head.atindex(idx)
  
  def decrypt(self):
    mod = len(self.order) 
    #print order, mod
    head = self.head
    #oldorder = [o for o in order]
    for node in self.order:
      sys.stdout.write('.')
      val = node.num
      if val == 0:
        pass
        #print 'Move', node, '(', node.num, ') does not move'
      elif val < 0:
        mval = abs(val)
        mval = mval % (mod - 1)
        #mval = ((mval-1) % mod) + 1
        #print 'Move', node, '(', node.num, ') left by', val, '(', mval, ')'
        node.move_left(mval)
      else:
        #mval = ((val-1) % mod) + 1
        mval = val
        mval = mval % (mod - 1)
        #print 'Move', node, '(', node.num, ') by', val, '(', mval, ')'
        node.move_right(mval)
      #self.head = head.find_head()
      #neworder = self.head.to_a()
      #print neworder
      #print 'Order', oldorder, '->', neworder
      #oldorder = neworder
    #self.head = head.find_head()

  def result_modcheck(self):
    nums = [1, 2, 3, 4, 5, 6, 7]
    print nums
    for n in range(10):
      num = n+1
      print num, 
    print

    size = len(nums)
    for n in range(10):
      num = n+1
      print (num % (size-1)),
    print

    for n in range(10):
      num = n+1
      print ((num-1) % size)+1,
    print

  def result(self):
    mod = len(self.order)
    print 'Count:', mod
    print 'Inflating Numbers:'
    for n in range(mod):
      self.order[n].num *= 811589153
    print self.head.to_a()
    print 'Decrypting'
    for rnd in range(10):
      print 'Round', rnd+1
      self.decrypt()
      #zero = self.head.find(0)
      #arr = zero.to_a()
      #print arr
    zero = self.head.find(0)
    total = 0
    for n in [1000, 2000, 3000]:
      #mval = n % mod
      num = zero.nth(n).num
      total += num
      print n, '->', num
    print 'Total', total

  def result1(self):
    mod = len(self.order)
    print 'Count:', mod
    self.decrypt()
    zero = self.head.find(0)
    total = 0
    for n in [1000, 2000, 3000]:
      num = zero.nth(n).num
      total += num
      print n, '->', num
    print 'Total', total



if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

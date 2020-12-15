import sys
class Puzzle:

  def process(self, text):
    self.nums = map(lambda n: int(n), text.split(','))
    #0, 3, 6 ->
    #-1, t=0, == 0: -1 => 0 :: t-map = n :> 0 - map[-1] => 0
    #0, t=1, == 3: 0 => -2  :: t-map = n :> 1 - map[ 0] => 3
    #3, t=2, == 6: 3 => -4  :: t-map = n :> 2 - map[ 3] => 6
    self.last = -1
    last = -1
    self.seen = {}
    self.t = 0
    for t in range(len(self.nums)):
      n = self.nums[t]
      m = -1 * (n-t)
      self.seen[last] = m
      last = n

  def next(self):
    #print self.t,': >', self.last, ':', self.seen
    if self.seen.has_key(self.last):
      #print 'Seen Last'
      tl = self.seen[self.last]
      n = self.t - tl
    else:
      #print 'Not Seen, ZERO'
      n = 0
    #print 'N>', n
    self.seen[self.last] = self.t 
    self.last = n
    self.t += 1
    return n

  def result(self):
    target = 30000000
    step = 100
    m = 0
    for i in range(step):
      for n in range(target / step):
        m = m + 1
        num = self.next()
      print m, ':>', num
      #print i+1, ':>', self.next()

if __name__ == '__main__':
  puz = Puzzle()
  str = sys.argv[1]
  puz.process(str)
  puz.result()

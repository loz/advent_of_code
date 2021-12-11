class Puzzle:
  
  def __init__(self):
    self.position = 0
    self.buffer = [0]

  def fast(self, steps, runs):
    num = 0
    pos = 0
    lastzero = 0
    for r in range(runs):
      num = num + 1
      newpos = (pos + steps) % num
      if newpos == 0:
        lastzero = num
      pos = newpos + 1

    return lastzero

  def spinlock(self, steps):
    newnumber = self.buffer[self.position] + 1
    position = self.position
    #spin around steps times
    position = (position + steps) % newnumber
    #print 'position', position
    #insert newnumber at this position
    left = self.buffer[:position+1]
    right = self.buffer[position+1:]
    #print left, right
    newbuffer = left + [newnumber] + right
    #print newbuffer
    self.buffer = newbuffer
    self.position = position + 1
    pass

  def result(self):
    #for i in range(50000000):
    #  self.spinlock(324)
    #print self.buffer[0], self.buffer[1]
    print self.fast(324, 50000000)

if __name__ == '__main__':
  puz = Puzzle()
  puz.result()

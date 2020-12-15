import hashlib
import re

START = r"(0{3}|1{3}|2{3}|3{3}|4{3}|5{3}|6{3}|7{3}|8{3}|9{3}|a{3}|b{3}|c{3}|d{3}|e{3}|f{3})"

class Puzzle:

  def process(self, salt):
    self.salt = salt
    self.index = 0
  
  def find_start(self):
    while True:
      text = self.salt + str(self.index)
      hash = hashlib.md5(text).hexdigest()
      #print hash
      #print '333' in hash
      match = re.findall(START, hash)
      self.index += 1
      if match:
        #print match
        #print hash, match.group(1), '@', self.index
        #ch = match.group(1)[0]
        return (self.index-1, match[0][0])

  def validKey(self, index, ch):
    target = ch * 5
    for i in range(index+1, index+1+1000):
      text = self.salt + str(i)
      hash = hashlib.md5(text).hexdigest()
      #print i, hash, target
      if target in hash:
        return True
    return False

  def result(self):
    numKeys = 0
    while numKeys <= 64:
      start = self.find_start()
      #print start
      idx, ch = start
      if self.validKey(idx, ch):
        numKeys += 1
        print 'Key', numKeys, idx

if __name__ == '__main__':
  puz = Puzzle()
  puz.process('jlmsuwbz')
  #puz.index = 8520
  #print puz.find_start()
  #puz.process('abc')
  puz.result()

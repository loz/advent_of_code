class Puzzle:

  def gendata(self, data):
    newdata = data + "0"
    newb = ''
    for ch in data:
      if ch == '1':
        newb = '0' + newb
      else:
        newb = '1' + newb
    return newdata + newb

  def gencsum(self, data):
    if len(data) % 2 != 0:
      return data
    newsum = ''
    i = 0
    while i < len(data):
      c1 = data[i]
      c2 = data[i+1]
      if c1 == c2:
        newsum += '1'
      else:
        newsum += '0'
      i += 2
    return self.gencsum(newsum)


  def result(self, data, target):
    while len(data) < target:
      data = self.gendata(data)
    #print len(data), 'bits generated'
    data = data [0:target]
    #print len(data), 'bits for checksum...'
    #print 'D:>', data
    csum = self.gencsum(data)
    #print target, len(csum), csum
    return csum
    #print len(csum), 'bits in checksum'

if __name__ == '__main__':
  val = '10010000000110000'
  val = int(val, 2)

  puz = Puzzle()
  print '====', val
  for i in range(0,20):
    sum = puz.result('10010000000110000', 17 * (2**i))
    isum = int(sum, 2)

    print sum, isum, '(', i, ',', (2**i), ',', 17 * (2**i), ')'
  #REPEATS @14, 2, @15, 3....
  #TARGET = 2**21, @21 = @9

 # puz.result('10010000000110000', n+2)
  #  n = n * 2
  print '====='
  #puz.result('10010000000110000', 35651584)
  target = 35651584
  original = target
  while target % 2 == 0:
    target = target / 2
  print 'Target (', original, ') Has', target, 'digits (x ', original / target, ')'

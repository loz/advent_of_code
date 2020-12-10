import copy

class Puzzle:

  def process(self, text):
    nums = map(lambda l: int(l), filter(lambda l: l.strip() != '', text.split('\n')))
    self.jolts = nums

  def differences(self, given=None):
    if given:
      ordered = given
    else:
      ordered = copy.copy(self.jolts)
      ordered.sort()
    diffs = []
    last = 0
    for n in ordered:
      diff = n - last
      diffs.append(diff)
      last = n
    diffs.append(3) #built in voltage adapter
    return diffs

  def _count_permutations(self, diffs):
    nn = len(diffs)
    if nn == 1:
      return 1
    n1 = diffs[0]
    if n1 == 3:
      return self._count_permutations(diffs[1:nn])
    n2 = diffs[1]
    if nn > 2:
      n3 = diffs[2]
      if n1 == 1 and n2 == 1 and n3 == 1:  # zip to, (1)11 | 12 | 21 | (3)
        b1= diffs[3:nn]  #(3)
        b2 = [2] + diffs[3:nn] #12
        b3 = [1] + diffs[3:nn] #(1)11 and 21
        return self._count_permutations(b1) \
               + self._count_permutations(b2) \
               + 2 * self._count_permutations(b3)
    if n1 == 1 and n2 == 1:  #zip to (1)1 | 2
      b1 = [1] + diffs[2:nn] #(1)1
      b2 = [2] + diffs[2:nn] #2
      return self._count_permutations(b1) \
             + self._count_permutations(b2)
    if n1 == 1 and n2 == 2:  #zip to (1)2 | 3
      b1 = diffs[2:nn]  #(3)
      b2 = [2] + diffs[2:nn] #(1)2
      return self._count_permutations(b1) \
             + self._count_permutations(b2)
    if n1 == 2 and n2 == 1: # zip to (2)1 | 3
      b1 = diffs[2:nn]  #3
      b2 = [1] + diffs[2:nn] #(2)1
      return self._count_permutations(b1) \
             + self._count_permutations(b2)
    #nm -> (n)m
    return self._count_permutations(diffs[1:nn])

  def count_permutations(self):
    diffs = self.differences()
    return self._count_permutations(diffs)


  def result2(self):
    diffs = self.differences()
    num1 = diffs.count(1)
    num3 = diffs.count(3)
    print "Num diff1: ", num1
    print "Num diff3: ", num3

  def result(self):
    print "Permutations:", self.count_permutations()

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

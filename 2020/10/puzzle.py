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

  def count_permutations_slow(self):
    diffs = self.differences()
    return self._count_permutations(diffs)

  def count_permutations(self):
    diffs = self.differences()
    runs = self.find_runs(diffs)
    print runs
    runs = filter(lambda r: r[0] > 1, runs)
    print runs
    perms = 1
    for run in runs:
      size, before, after = run
      perm = 1 + int(((size-1)/2.0) * size) 
      if before == 2:
        perm = perm + 1
      if after == 2:
        perm = perm + 1
      perms = perm * perms
    return perms

  def find_runs(self, diffs):
    isRun = False
    count = 0
    previous = None
    runs = []
    for n in diffs:
      if isRun:
        if n == 1:
          count = count + 1
        else:
          #Run ended
          run = (count, previous, n)
          runs.append(run)
          count = 0
          isRun = False
          previous = n
      else:
        if n == 1:
          #Run starting
          count = 1
          isRun = True
        else:
          previous = n
    return runs

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

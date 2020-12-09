import itertools
import sys

class Puzzle:

  def process(self, text):
    lines = filter(lambda l: l.strip() != '', text.split('\n'))
    lines = map(lambda l: int(l), lines)
    self.cursor = 0
    self.numbers = lines

  def take(self, preamble):
    if self.cursor < preamble:
      self.cursor = preamble
    number = self.numbers[self.cursor]
    precede = self.numbers[self.cursor-preamble:self.cursor]
    comb = itertools.combinations(precede, 2)
    comb = map(lambda c: c[0] + c[1], comb)
    #print number, ':', precede, '>', comb, len(precede)
    isValid = number in comb
    self.cursor = self.cursor + 1
    return (number, isValid)

  def result(self):
    n, isValid = self.take(25)
    while isValid:
      print n, isValid
      n, isValid = self.take(25)
    print "Ends: ", n, isValid

  def result2(self):
    target = 26796446
    runsize = len(self.numbers)
    searching = True
    while searching:
      print "Trying run of", runsize
      runs = self.build_runs(runsize)
      sums = map(lambda r: (sum(r), r), runs)
      for sumItem in sums:
        n, run = sumItem
        if n == target:
          print "Found!", run
          print "Min", min(run)
          print "Max", max(run)
          print "Sum", min(run) + max(run)
          searching = False
      runsize = runsize - 1

  def build_runs(self, size):
    start = 0
    end = size
    maxN = len(self.numbers)
    runs = []
    while end <= maxN:
      runs.append(self.numbers[start:end])
      start = start + 1
      end = end + 1
    return runs

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result2()

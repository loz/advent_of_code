import sys
from colorama import Fore
from functools import reduce
import re

class Puzzle:
  
  def __init__(self):
    self._rows = []
    self.problems = []

  def process(self, text):
    for line in text.split('\n'):
      self.process_line(line)

    tlist = list(map(list, zip(*self._rows)))
    self.problems = list(map(lambda x: (self.makeInts(x[:-1]), x[-1]), tlist))

  def process2(self, text):
    rows = []
    for line in text.split('\n'):
      if line != '':
        rows.append(list(ch for ch in line))
    tlist = list(map(list, zip(*rows)))
    problems = []
    new = True
    numbers = []
    for item in tlist:
      if new:
        nums = item[:-1]
        op = item[-1]
        nums = filter(lambda x: x != ' ', nums)
        nums = ''.join(nums)
        num = int(nums)
        numbers.append(num)
        new = False
      else:
        nums = list(filter(lambda x: x != ' ', item))
        if len(nums) == 0:
          problems.append((numbers, op))
          numbers = []
          new = True
        else:
          num = int(''.join(nums))
          numbers.append(num)
    problems.append((numbers, op))
    self.problems = problems
        
      

  def makeInts(self, items):
    return list(map(int, items))

  def process_line(self, line):
    if line != '':
      vals = re.split(r'\s+', line)
      vals = list(filter(lambda x: x != '', vals))
      self._rows.append(vals)

  def eval_problem(self, problem):
    nums, op = problem
    if op == '+':
      return reduce(lambda v,e: v + e, nums, 0)
    elif op == '*':
      return reduce(lambda v,e: v * e, nums, 1)


  def result1(self):
    total = 0
    for problem in self.problems:
      result = self.eval_problem(problem) * 1
      print(problem, result)
      total += result
    print('Total:', total)

  def result(self):
    self.result1()


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process2(inp)
  puz.result()

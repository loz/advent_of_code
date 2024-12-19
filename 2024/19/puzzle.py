import sys
from colorama import Fore
from functools import cmp_to_key


def cmp_len(a, b):
  return len(b) - len(a)
  #return len(a) - len(b)

class Puzzle:

  def process(self, text):
    self.towels = []
    self.patterns= []
    self.seen_chunks = {}

    towels, patterns = text.split('\n\n')

    self.process_towels(towels)
    self.process_patterns(patterns)
    self.patterns = sorted(self.patterns, key=cmp_to_key(cmp_len))
    #print(self.patterns)


  def process_towels(self, towels):
    self.towels = towels.split(', ')

  def process_patterns(self, patterns):
    for line in patterns.split('\n'):
      if line != '':
        self.patterns.append(line)

  def _r_valid_combos(self, pattern):
    if pattern == '':
      return 1

    if pattern in self.seen_chunks:
      return self.seen_chunks[pattern]

    count = 0
    for towel in self.towels:
      if len(towel) > len(pattern):
        next
      if pattern.startswith(towel):
        rest = pattern[len(towel):]
        #print(towel, ':', rest, '=', pattern)
        count += self._r_valid_combos(rest)
    self.seen_chunks[pattern] = count
    return count

  def valid_combos(self, pattern):
    self.seen_chunks = {}
    return self._r_valid_combos(pattern)

  def _r_valid(self, pattern):
    if pattern == '':
      return True

    if pattern in self.seen_chunks:
      return self.seen_chunks[pattern]

    for towel in self.towels:
      if len(towel) > len(pattern):
        next

      if pattern.startswith(towel):
        rest = pattern[len(towel):]
        #print(towel, ':', rest, '=', pattern )
        if self._r_valid(rest):
          self.seen_chunks[pattern] = True
          return True
        else:
          self.seen_chunks[pattern] = False
    return False

  def valid_pattern(self, pattern):
    return self._r_valid(pattern)


  def result(self):
    total = 0
    for pattern in self.patterns:
      count = self.valid_combos(pattern)
      print(pattern, count)
      total += count
    print('Total Valid:', total)

  def result1(self):
    total = 0
    for pattern in self.patterns:
      isvalid = self._r_valid(pattern)
      if isvalid:
        print(pattern, 'valid')
        total += 1
      else:
        print(pattern)
    print('Total Valid:', total)

if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

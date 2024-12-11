import sys
from colorama import Fore

class Puzzle:

  def process(self, text):
    self.stones = []
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      self.stones = [int(ch) for ch in line.split()]

  def blink(self, stones):
    newstones = []
    for stone in stones:
      if stone == 0:
        newstones.append(stone + 1)
      else:
        txt = str(stone)
        if len(txt) % 2 == 0:
          left = txt[:len(txt)//2]
          right = txt[len(txt)//2:]
          newstones.append(int(left))
          newstones.append(int(right))
        else:
          newstones.append(stone * 2024)
    return newstones

  def blink_a_stone(self, stone):
    newstones = []
    if stone == 0:
      newstones.append(stone + 1)
    else:
      txt = str(stone)
      if len(txt) % 2 == 0:
        left = txt[:len(txt)//2]
        right = txt[len(txt)//2:]
        newstones.append(int(left))
        newstones.append(int(right))
      else:
        newstones.append(stone * 2024)
    return newstones

  def blink_n(self, n, stones, cache = {}):
    #cache = {} #children at N depth -> count
    total = 0
    if n == 0:
      return len(stones)
    for stone in stones:
      if (stone, n) in cache:
        #print('.', end='', flush=True)
        total += cache[(stone, n)]
      else:
        children = self.blink_a_stone(stone)
        count = self.blink_n(n-1, children, cache)
        cache[(stone, n)] = count
        total += count
    return total

  def result(self):
    stones = self.stones
    print(stones)
    #count = self.blink_n(25, stones)
    count = self.blink_n(75, stones)
    print('Total Stones:', count)

  def result1(self):
    stones = self.stones
    print(stones)
    for n in range(25):
      stones = self.blink(stones)
      print(n, stones)
    print('Total Stones:', len(stones))


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

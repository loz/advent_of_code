import sys
from colorama import Fore

class Puzzle:

  def __init__(self):
    self.locks = []
    self.keys = []

  def process(self, text):
    schematics = text.split('\n\n')
    for schematic in schematics:
      self.process_schematic(schematic)

  def process_schematic(self, schematic):
    schematic = schematic.strip()
    lines = schematic.split('\n')
    if lines[0] == '#####': #lock
      lock = self.decode(lines[1:])
      self.locks.append(lock)
    else:
      key = self.decode(lines[:-1])
      self.keys.append(key)

  def decode(self, lines):
    item = [0, 0, 0, 0, 0]
    for row in lines:
      for col, ch in enumerate(row):
        if ch == '#':
          item[col] += 1
    return tuple(item)

  def fits(self, lock, key):
    for x, lv in enumerate(lock):
      kv = key[x]
      if lv + kv > 5:
        return False
    return True

  def result(self):
    total = 0
    for key in self.keys:
      for lock in self.locks:
        if self.fits(lock, key):
          total += 1
    print('Total Fitting:', total)


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

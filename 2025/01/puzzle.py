import sys
from colorama import Fore

class Puzzle:

  def __init__(self):
    self.position = 50
    self.zero_count = 0
    self.count_clicks = False

  def process(self, text):
    for line in text.split('\n'):
      self.process_line(line)

  def set0x434C49434B(self):
    self.count_clicks = True

  def process_line(self, line):
    line = line.strip()
    if line == '':
      return
    direction = line[0]
    value = int(line[1:])
    self.rotate(direction, value)

  def rotate(self, direction, value):
    position = self.position
    if direction == 'L':
      d = -1
    else:
      d = +1

    for n in range(value):
      position += d
      if position < 0:
        position = 100+position
      if position > 99:
        position = 100-position
      if position == 0:
        self.zero_count += 1

    self.position = position
    print('The dial is rotate', direction, value, 'to point at', self.position, '=>', self.zero_count)


  def result(self):
    print('Processed', self.zero_count)


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.set0x434C49434B()
  puz.process(inp)
  puz.result()

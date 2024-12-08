import sys
from colorama import Fore
import itertools

class Puzzle:

  def process(self, text):
    self.antenae = {}
    for y, line in enumerate(text.split('\n')):
      self.process_line(y, line)
    self.map_height = y - 1

  def process_line(self, y, line):
    if line != '':
      for x, ch in enumerate(line):
        if ch != '.':
          locs = self.antenae.get(ch, [])
          locs.append((x, y))
          self.antenae[ch] = locs
      self.map_width = x

  def resonant_antinodes(self, ch):
    antinodes = []
    nodes = self.antenae[ch]
    pairs = itertools.combinations(nodes, 2)
    for pair in pairs:
      a1, a2 = pair
      dx, dy = a1[0]-a2[0], a1[1]-a2[1]
      nx, ny = (a1[0]+dx, a1[1]+dy)
      while nx in range(self.map_width+1) and ny in range(self.map_height+1):
        antinodes.append((nx, ny))
        nx, ny = (nx+dx, ny+dy)

      nx, ny = (a2[0]-dx, a2[1]-dy)
      while nx in range(self.map_width+1) and ny in range(self.map_height+1):
        antinodes.append((nx, ny))
        nx, ny = (nx-dx, ny-dy)

    return antinodes

  def antinodes(self, ch):
    antinodes = []
    nodes = self.antenae[ch]
    pairs = itertools.combinations(nodes, 2)
    for pair in pairs:
      a1, a2 = pair
      dx, dy = a1[0]-a2[0], a1[1]-a2[1]
      nx, ny = (a1[0]+dx, a1[1]+dy)
      if nx in range(self.map_width+1) and ny in range(self.map_height+1):
        antinodes.append((nx, ny))
      nx, ny = (a2[0]-dx, a2[1]-dy)
      if nx in range(self.map_width+1) and ny in range(self.map_height+1):
        antinodes.append((nx, ny))
    return antinodes

  def print_debug(self, antinodes):
    mapnodes = {}
    for ch in self.antenae:
      nodes = self.antenae[ch]
      for pos in nodes:
        mapnodes[pos] = ch
    for y in range(self.map_height+1):
      for x in range(self.map_width+1):
        if (x,y) in mapnodes:
          print(Fore.CYAN + mapnodes[(x,y)] + Fore.RESET, end='')
        elif (x,y) in antinodes:
          print(Fore.YELLOW + '#' + Fore.RESET, end='')
        else:
          print('.', end='')
      print('')

  def result(self):
    anodes = set()
    for ch in self.antenae:
      nodes = self.resonant_antinodes(ch)
      if len(self.antenae[ch]) > 1:
        anodes |= set(self.antenae[ch])
      anodes |= set(nodes)
    anodes = list(anodes)
    self.print_debug(anodes)
    print('Unique:', len(anodes))

  def result1(self):
    anodes = set()
    for ch in self.antenae:
      nodes = self.antinodes(ch)
      anodes |= set(nodes)
    anodes = list(anodes)
    self.print_debug(anodes)
    print('Unique:', len(anodes))

if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

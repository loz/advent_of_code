import sys
from colorama import Fore
from itertools import product, combinations


def rotate_shape(shape):
  rows = []
  for row in shape:
    cols = [ch for ch in row]
    rows.append(cols)
  rotated = zip(*rows[::-1])
  nshape = []
  for row in rotated:
    nshape.append(''.join(row))
  return nshape

def flip_shape(shape):
  nshape = []
  for row in shape:
    cols = [ch for ch in row]
    cols.reverse()
    nshape.append(''.join(cols))
  return nshape
 
def fit_shape(shape, matrix, ox, oy):
  y = 0
  for row in shape:
    x = 0
    for ch in row:
      if ch == '#':
        if matrix[y+oy][x+ox] != '.':
          return False
      x += 1
    y += 1
  nmatrix = [row[:] for row in matrix]
  y = 0
  #print('Fit', ox, oy)
  #print('\n'.join(shape))
  #print('In')
  #print('----')
  #for row in matrix:
  #  print(''.join(row))
  for row in shape:
    x = 0
    for ch in row:
      if ch == '#':
        nmatrix[y+oy][x+ox] = '#'
      x += 1
    y += 1
  #print('----')
  #for row in nmatrix:
  #  print(''.join(row))
  return nmatrix

class Puzzle:
  
  def __init__(self):
    self.shapes = {}
    self.permutations = {}
    self.regions = []

  def process(self, text):
    parts = text.split('\n\n')
    self.process_shapes(parts[0:-1])
    self.process_regions(parts[-1])
    
  def process_shapes(self, parts):
    for part in parts:
      idx, right = part.split(':\n')
      idx = int(idx)
      shape = right.split('\n')
      self.shapes[idx] = shape

  def process_regions(self, text):
    lines = text.split('\n')
    for line in lines:
      if line != '':
        left, right = line.split(': ')
        x, y = left.split('x')
        x = int(x)
        y = int(y)
        counts = right.split(' ')
        counts = list(map(int, counts))
        self.regions.append(((x,y), counts))

  def get_permutations(self, idx):
    if idx in self.permutations:
      return self.permutations[idx]

    shape = self.shapes[idx]
    perms = [shape]
    for i in range(3):
      shape = rotate_shape(shape)
      if shape not in perms:
        perms.append(shape)
      fshape = flip_shape(shape)
      if fshape not in perms:
        perms.append(fshape)
    
    self.permutations[idx] = perms
    return perms

  def get_shape(self, idx):
    shape = self.shapes[idx]
    return shape

  def expand_present_list(self, plist):
    items = []
    for idx in range(len(plist)):
      count = plist[idx]
      for c in range(count):
        items.append(idx)
    return items

  def pile_needs(self, pile):
    total = 0
    for s in pile:
      shape = self.shapes[s]
      total += sum(row.count('#') for row in shape)
    return total

  def _fits_remaining(self, pile, matrix, mx, my, cache):
    if pile:
      cache[(tuple(''.join(row) for row in matrix), tuple(pile))] = True
      empty = sum(row.count('.') for row in matrix)
      needed = self.pile_needs(pile)
      if empty < needed:
        return False
      pitem = pile[0]
      rest = pile[1:]
      variations = self.get_permutations(pitem)
      d = len(variations[0])
      #print(mx, my, 'vs', d)
      for v in variations:
        #print(v)
        for y in range(my-d+1):
          for x in range(mx-d+1):
            newmatrix = fit_shape(v, matrix, x, y)
            if newmatrix:
              if (tuple(''.join(row) for row in newmatrix), tuple(rest)) in cache:
                continue
              if self._fits_remaining(rest, newmatrix, mx, my, cache):
                return True
      return False
    else:
      return True
  
  def does_pile_fit(self, pile, region):
    x, y = region
    matrix = [['.'] * x for _ in range(y)]
    return self._fits_remaining(pile, matrix, x, y, {})

  def result(self):
    total = 0
    for region in self.regions:
      size, presents = region
      pile = self.expand_present_list(presents)
      fits = self.does_pile_fit(pile, size)
      if fits:
        total += 1
      print(size, presents, fits)
    print('Total fitting:', total)




if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

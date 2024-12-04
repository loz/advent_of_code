import sys
from colorama import Fore
import itertools

class Puzzle:

  def process(self, text):
    self.words = []
    self.grid = []
    for line in text.split('\n'):
      self.process_line(line)
    self.scan_for_words()

  def process_line(self, line):
    if line != '':
      self.grid.append([ch for ch in line])

  def scan_for_words(self):
    self.scan_for_target(['X', 'M', 'A', 'S'])
    self.scan_for_target(['S', 'A', 'M', 'X'], direction = -1)

  def scan_horizontal(self, target, direction):
    for y in range(len(self.grid)):
      line = self.grid[y]
      offset = 0
      for x in range(0, len(line)):
        #print('?', line[x], target[offset], end='')
        if line[x] == target[offset]:
            if offset == len(target)-1:
               if direction == 1:
                 start = (x-offset, y)
                 end = (x, y)
               else:
                 end = (x-offset, y)
                 start = (x, y)
               #print('Found', start, end)
               self.words.append((start, end))
               offset = 0
            else:
               offset += 1
        elif line[x] == target[0]: #restart match
          offset = 1
        else:
          #cease to match
          offset = 0
      #print('')

  def scan_vertical(self, target, direction):
    for x in range(len(self.grid[0])):
      offset = 0
      for y in range(len(self.grid)):
        #print('?', line[x], target[offset], end='')
        if self.grid[y][x] == target[offset]:
            if offset == len(target)-1:
               if direction == 1:
                 start = (x, y-offset)
                 end = (x, y)
               else:
                 end = (x, y-offset)
                 start = (x, y)

               #print('Found', start, end)
               self.words.append((start, end))
               offset = 0
            else:
               offset += 1
        elif self.grid[y][x] == target[0]: #restart match
          offset = 1
        else:
          #cease to match
          offset = 0
      #print('')

  def scan_back_slash(self, target, direction):
    #\ Diagonal
    for x in range(len(target)-1, len(self.grid[0])):
      for y in range(len(self.grid)-len(target)+1):
        #print('?', line[x], target[offset], end='')
        if self.grid[y][x] == target[0]:
           found = True
           for offset in range(1, len(target)):
              if not self.grid[y+offset][x-offset] == target[offset]:
                 found = False
                 break;
            #matching
           if found:
              if direction == 1:
                start = (x, y)
                end = (x-offset, y+offset)
              else:
                end = (x, y)
                start = (x-offset, y+offset)
              #print('Found', start, end)
              self.words.append((start, end))
      #print('')

  def scan_forward_slash(self, target, direction):
    #\ Diagonal
    for x in range(len(self.grid[0])-len(target)+1):
      for y in range(len(self.grid)-len(target)+1):
        #print('?', line[x], target[offset], end='')
        if self.grid[y][x] == target[0]:
           found = True
           for offset in range(1, len(target)):
              if not self.grid[y+offset][x+offset] == target[offset]:
                 found = False
                 break;
            #matching
           if found:
              if direction == 1:
                start = (x, y)
                end = (x+offset, y+offset)
              else:
                end = (x, y)
                start = (x+offset, y+offset)
              #print('Found', start, end)
              self.words.append((start, end))
      #print('')

  def scan_for_target(self, target, direction=1):
      self.scan_horizontal(target, direction)
      self.scan_vertical(target, direction)
      self.scan_forward_slash(target, direction)
      self.scan_back_slash(target, direction)

  def print_debug(self):
    target = 'XMAS'
    letters = {}
    for word in self.words:
      start, end = word
      direction = 1
      if start[0] == end[0]: #V
         if start[1] > end[1]:
            direction = -1
         for i in range(len(target)):
            letters[(start[0],start[1]+(i*direction))] = True
      elif start[1] == end[1]: #H
         if start[0] > end[0]:
            direction = -1
         for i in range(len(target)):
            letters[(start[0]+(i*direction),start[1])] = True
      else: #Diag
         dx, dy = 1, 1
         if start[0] > end[0]:
            dx = -1
         if start[1] > end[1]:
            dy = -1
         for i in range(len(target)):
            letters[(start[0]+(i*dx),start[1]+(i*dy))] = True

    for y in range(len(self.grid)):
      for x in range(len(self.grid[0])):
         if letters.get((x,y), False):
            print(Fore.GREEN + self.grid[y][x], end='')
         else:
            print(Fore.RESET + self.grid[y][x], end='')
      print(Fore.RESET + '')

  def normalize_words(self, words):
     wrds = []
     for word in words:
       start, end = word
       if start[0] > end[0]:
         wrds.append((end, start))
       else:
         wrds.append((start, end))
     return wrds

  def find_pairs(self, words):
     #a: (x, y) -> (x2, y2)
     #b: (x, y2) -> (x2, y)
     found = []
     pairs = itertools.combinations(words, 2)
     for pair in pairs:
        a, b = pair
        #print(a,b)
        (ax1, ay1), (ax2, ay2) = a
        (bx1, by1), (bx2, by2) = b
        if min(ax1,ax2) == min(bx1,bx2) and \
           max(ax1,ax2) == max(bx1,bx2) and \
           min(ay1,ay2) == min(by1,by2) and \
           max(ay1,ay2) == max(by1,by2):
             found.append(pair)
     return found

  def find_cross(self, text):
    pairs = []
    target = [ch for ch in text]
    target2 = target.copy()
    target2.reverse()
    targets = [target, target2]
    self.words = []
    for target in targets:
      self.scan_forward_slash(target, 1) 
      self.scan_back_slash(target, 1) 
    pairs = self.find_pairs(self.words)
    return pairs

  def result(self):
     pairs = self.find_cross('MAS')
     self.words = []
     for pair in pairs:
        a, b = pair
        self.words.append(a)
        self.words.append(b)
     self.print_debug()
     print('Total Found:', len(pairs))

  def result1(self):
     self.print_debug()
     print('Total Found:', len(self.words))


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

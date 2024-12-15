import sys
from colorama import Fore

class Puzzle:

  def process(self, text):
    self.robots = []
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      left, right = line.split(' ')
      _, left = left.split('=')
      _, right = right.split('=')
      x, y = left.split(',')
      pos = (int(x),int(y))
      x, y = right.split(',')
      vel = (int(x),int(y))
      self.robots.append((pos, vel))

  def move_robots(self, robots, width, height, n=1):
    nrobots = []
    for robot in robots:
      pos, vel = robot
      x, y = pos
      dx, dy = vel
      nx = (x + n*dx) % width
      ny = (y + n*dy) % height
      nrobots.append( ((nx, ny), vel) )
    return nrobots

  def count_quadrants(self, robots, width, height):
    xmid = width // 2
    ymid = height // 2
    tl = 0
    tr = 0
    bl = 0
    br = 0
    for pos, vel in robots:
      x, y = pos
      if x < xmid:     #L
        if y < ymid:   #TL
          tl += 1
        elif y > ymid: #BL
          bl += 1
      elif x > xmid:   #R
        if y < ymid:   #TR
          tr += 1
        elif y > ymid: #BR
          br += 1

    return [tl, tr, bl, br]


  def print_debug(self, robots, width, height):
    xmid = width // 2
    ymid = height // 2
    rmap = {}
    #print(u"\u001b[H")
    print('='*103)
    for pos, vel in robots:
      if pos in rmap:
        rmap[pos] += 1
      else:
        rmap[pos] = 1

    for y in range(height):
      if y == ymid:
        print(Fore.CYAN, end='')
      for x in range(width):
        if x == xmid:
          print(Fore.CYAN, end='')
        
        if (x,y) in rmap:
          print(rmap[x,y], end='')
        else:
          print('.', end='')

        if x == xmid and y != ymid:
          print(Fore.RESET, end='')
      if y == ymid:
        print(Fore.RESET, end='')
      print('')

    pass

  def result(self):
    seen = {}
    robots = self.robots

    notFound = True

    width = 101
    height = 103
    
    robots = self.move_robots(self.robots, width, height, 7569)
    self.print_debug(robots, width, height)
    return 

    """
    t = 0
    while notFound:
      seen[str(robots)] = True
      robots = self.move_robots(robots, width, height)
      t += 1
      if t % 10000 == 0:
        print('T', t)
      if str(robots) in seen:
        print('Found', t)
        notFound = False
    #"""

    #print('Loops at ', width*height)

    #return 

    mincluster = 10000000000000000
    minset = []
    mint = None
    for t in range((width*height)+1):
      robots = self.move_robots(self.robots, width, height, t)
      self.print_debug(robots, width, height)
      print('T', t)

  def result1(self):
    robots = self.robots
    width = 101
    height = 103
    #Converges ~ H:50  153 256 ?359 ?  +103,
    #            V:95  196 + 101
    #for s in range(1105): #95+105):
    #  robots = self.move_robots(robots, width, height)
    #self.print_debug(robots, width, height)
    #return

    #n = 50+ 7579*(103*101)
    #n= 103000000050
    #n= 1066464545

    #robots = self.robots
    #robots = self.move_robots(robots, width, height, n)
      
    #self.print_debug(robots, width, height)
    #return 

    #n = 50

    for s in range(1000000):
      robots = self.move_robots(self.robots, width, height, s)
      self.print_debug(robots, width, height)
      print('ROUND:', s)
      for x in range(1000000):
        for y in range(10):
          z = x*y*1000

  def result1(self):
    robots = self.robots
    width = 101
    height = 103
    for s in range(100):
      robots = self.move_robots(robots, width, height)
    self.print_debug(robots, width, height)
    quads = self.count_quadrants(robots, width, height)
    print('Quadrants:', quads)
    total = 1
    for q in quads:
      total *= q
    print('Saftey Factor:', total)

if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

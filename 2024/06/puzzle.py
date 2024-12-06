import sys
from colorama import Fore

DIRECTIONS = {
  '^': (0,-1),
  '>': (1, 0),
  'v': (0, 1),
  '<': (-1,0)
}

TURNS = {
  '^': '>',
  '>': 'v',
  'v': '<',
  '<': '^'
}

class Puzzle:

   def process(self, text):
      self.obstacles = []
      self.map = []
      for line in text.split('\n'):
         self.process_line(line)
      self.width = len(self.map[0])
      self.height = len(self.map)
      self.locate_obstacles_and_guard()
      self.map_obstacles()

   def map_obstacles(self):
      self.obstacle_map = {}
      for obs in self.obstacles:
         self.obstacle_map[obs] = True

   def locate_obstacles_and_guard(self):
      for y,row in enumerate(self.map):
         for x, ch in enumerate(row):
            if ch == '#':
               self.obstacles.append((x,y))
            elif ch in ['^', '>']:
               self.guard_location = (x, y, ch)

   def process_line(self, line):
      if line != '':
         self.map.append([ch for ch in line])

   def guard_will_leave(self):
      original = self.guard_location
      visited = {}
      current = self.guard_location
      while current not in visited and current != None:
         visited[current] = True
         self.move_guard()
         current = self.guard_location
      self.guard_location = original
      return (current == None)

   def move_guard(self):
      x, y, d = self.guard_location
      nx, ny, nd = x, y, d

      dx, dy = DIRECTIONS[d]
      ny = y+dy
      nx = x+dx
      if self.obstacle_map.get((nx,ny), False):
         ny = y
         nx = x
         nd = TURNS[d]
      if nx not in range(self.width) or ny not in range(self.height):
         self.guard_location = None
      else:
         self.guard_location = (nx, ny, nd)

   def guard_walk_map(self):
      original = self.guard_location
      visited = {}
      x, y, _ = self.guard_location
      visited[(x,y)] = True
      while self.guard_location:
         self.move_guard()
         if self.guard_location:
            x, y, _ = self.guard_location
            visited[(x,y)] = True
      self.guard_location = original
      return list(visited.keys())
      

   def result(self):
      #For each location the guard usually walks
      #Insert an obstacle
      #Check it
      visited = self.guard_walk_map()
      locations = []
      for loc in visited:
         print('.', end='', flush=True)
         self.obstacle_map[loc] = True
         if not self.guard_will_leave():
            locations.append(loc)
         self.obstacle_map[loc] = False
      print('')
      print('Total Locations:', len(locations))

   def result1(self):
      visited = self.guard_walk_map()
      print('Total Locations:', len(visited))

if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

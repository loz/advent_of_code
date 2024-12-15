import sys
from colorama import Fore


DIRECTIONS = {
  '<': (-1, 0),
  '>': ( 1, 0),
  '^': ( 0,-1),
  'v': ( 0, 1)
}

GLIPHS = {
  1: {
    'O': 'O',
  },
  2: {
    'O': '[',
  }
}

class Puzzle:

  def process(self, text):
    maptext, orders = text.split('\n\n')
    self.process_map(maptext)
    self.process_orders(orders)
    self.current_order = 0

  def process_orders(self, text):
    orders = ''
    for line in text.split('\n'):
      orders += line
    self.orders = orders
  
  def process_map(self, text):
    self.boxes = []
    self.rightboxes = []
    self.walls = []

    y = 0
    for line in text.split('\n'):
      if line != '':
        self.width = len(line)
        for x, ch in enumerate(line):
          if ch == 'O':
            self.boxes.append( (x,y) )
          elif ch == '@':
            self.robot = (x, y)
          elif ch == '#':
            self.walls.append( (x,y) ) 
        y += 1
    self.height = y


  def push_left(self, x, y):
    #  []< or [].< or #<
    if (x,y) in self.rightboxes:
      boxes = []
      cx = x
      while (cx,y) in self.rightboxes:
        boxes.append((cx,y))
        cx-=2
      #We have hit a space or wall
      if (cx,y) in self.walls:
        return False #Cannot push
      else:
        #Move all the boxes
        for box in boxes:
          rbx, rby = box
          lbx, lby = rbx-1, rby

          self.rightboxes.remove((rbx, rby))
          self.rightboxes.append((rbx-1, rby))

          self.boxes.remove((lbx, lby))
          self.boxes.append((lbx-1, lby))
        return True
    elif (x,y) in self.walls:
      return False
    else:
      return True

  def push_right(self, x, y):
    # >[] or >.[] or >#
    if (x,y) in self.boxes:
      boxes = []
      cx = x
      while (cx,y) in self.boxes:
        boxes.append((cx,y))
        cx+=2
      #We have hit a space or wall
      if (cx,y) in self.walls:
        return False #Cannot push
      else:
        #Move all the boxes
        for box in boxes:
          lbx, lby = box
          rbx, rby = lbx+1, lby

          self.rightboxes.remove((rbx, rby))
          self.rightboxes.append((rbx+1, rby))

          self.boxes.remove((lbx, lby))
          self.boxes.append((lbx+1, lby))
        return True
    elif (x,y) in self.walls:
      return False
    else:
      return True

  def r_impact_up(self, x, y):
    if (x,y) in self.walls:
      return []
    if (x,y) in self.boxes: #Pushing left of a box
      rx = x + 1
      lx = x

      lboxes = [(lx,y), (rx,y)] + self.r_impact_up(lx, y-1)
      rboxes = self.r_impact_up(rx, y-1)
    elif (x,y) in self.rightboxes: #Pushng right of a box
      rx = x
      lx = x - 1
      lboxes = self.r_impact_up(lx, y-1)
      rboxes = [(lx, y), (rx,y)] + self.r_impact_up(rx, y-1)
    else:
      return []

    return lboxes + rboxes

  def r_impact_down(self, x, y):
    if (x,y) in self.walls:
      return []

    if (x,y) in self.boxes: #Pushing left of a box
      rx = x + 1
      lx = x

      lboxes = [(lx,y), (rx,y)] + self.r_impact_down(lx, y+1)
      rboxes = self.r_impact_down(rx, y+1)
    elif (x,y) in self.rightboxes: #Pushng right of a box
      rx = x
      lx = x - 1
      lboxes = self.r_impact_down(lx, y+1)
      rboxes = [(lx, y), (rx,y)] + self.r_impact_down(rx, y+1)
    else:
      return []

    return lboxes + rboxes
    
  def push_down(self, x, y):
    boxes = list(set(self.r_impact_down(x,y)))
    #Check if all impacted CAN move
    for box in boxes:
      blw_x, blw_y = box[0], box[1] + 1
      if (blw_x, blw_y) in self.walls:
        return False

    lefts = []
    rights = []
    for box in boxes:
      if box in self.boxes:
        self.boxes.remove(box)
        lefts.append((box[0], box[1]+1))
      else:
        self.rightboxes.remove(box)
        rights.append((box[0], box[1]+1))
    for left in lefts:
      self.boxes.append(left)
    for right in rights:
      self.rightboxes.append(right)

    return True

  def push_up(self, x, y):
    boxes = list(set(self.r_impact_up(x,y)))
    #print('Impacted:', boxes)
    #Check if all impacted CAN move
    for box in boxes:
      blw_x, blw_y = box[0], box[1] -1
      if (blw_x, blw_y) in self.walls:
        return False

    lefts = []
    rights = []
    for box in boxes:
      if box in self.boxes:
        self.boxes.remove(box)
        lefts.append((box[0], box[1]-1))
      else:
        self.rightboxes.remove(box)
        rights.append((box[0], box[1]-1))
    for left in lefts:
      self.boxes.append(left)
    for right in rights:
      self.rightboxes.append(right)

    return True

  """

  >[]  
  []<

  v
  []
   v
  []

  []
  ^

  []
   ^

  Possible
  v
  []
   []
    []
     []
      ..

  #Possible (down/up)
      v
      []
     [][]
    []  []

  """

  def push_boxes(self, x, y, dx, dy, robot=False):
    scale = (self.scale == 2)
    if scale:
      if dy == 0: #LEFT/RIGHT
        if dx <0 : #LEFT
          return self.push_left(x-1, y)
        else:
          return self.push_right(x+1, y)
      else: #UP/DOWN
        if dy < 0:
          return self.push_up(x, y-1)
        else:
          return self.push_down(x, y+1)
    else:
      if (x, y) in self.boxes:
        nbx, nby = (x + dx, y+dy)
        if (nbx, nby) in self.walls:
          return False
        
        if self.push_boxes(nbx, nby, dx, dy):
          self.boxes.remove((x,y))
          self.boxes.append((nbx, nby))
          return True
        return False
      else:
        return True


  def remaining_orders(self):
    return self.current_order < len(self.orders)

  def move_robot(self):
    d = self.orders[self.current_order]
    dx, dy = DIRECTIONS[d]
    x, y = self.robot
    nx, ny = x + dx, y + dy
    self.current_order += 1

    if (nx, ny) in self.walls:
      return

    if self.push_boxes(x, y, dx, dy):
      self.robot = (nx, ny)

  def dump_map(self):
    for y in range(self.height):
      for x in range(self.width):
        if (x,y) in self.walls:
          print(Fore.RED + '#' + Fore.RESET, end='')
        elif (x,y) in self.boxes:
          print(Fore.YELLOW + GLIPHS[self.scale]['O'] + Fore.RESET, end='')
        elif (x,y) in self.rightboxes:
          print(Fore.YELLOW + ']' + Fore.RESET, end='')
        elif self.robot == (x,y):
          print(Fore.CYAN + '@' + Fore.RESET, end='')
        else:
          print('.', end='')
      print('')

  def scale(self):
    self.scale = 2
    self.width = self.width*2

    #Add Twice Walls for ease of collision detection
    walls = []
    for wall in self.walls:
      walls.append( (wall[0]*2, wall[1]) )
      walls.append( ((wall[0]*2)+1, wall[1]) )
    self.walls = walls

    boxes = []
    rightboxes = []
    for box in self.boxes:
      boxes.append( (box[0]*2, box[1]) )
      rightboxes.append( ((box[0]*2)+1, box[1]) )
    self.boxes = boxes
    self.rightboxes = rightboxes
    
    self.robot = (self.robot[0] * 2, self.robot[1])


  def result(self):
    self.scale()
    print('Initial State:')
    self.dump_map()
    while self.remaining_orders():
      #print('Move', self.orders[self.current_order])
      self.move_robot()
      #self.dump_map()
      #print('')
    self.dump_map()
    total = 0
    for box in self.boxes:
      x, y = box
      total += ((100 *y) + x)
    print('GPS Total:', total)

  def result1(self):
    #print('Initial State:')
    #self.dump_map()
    while self.remaining_orders():
      #print('Move', self.orders[self.current_order])
      self.move_robot()
      #self.dump_map()
      #print('')

    self.dump_map()

    total = 0
    for box in self.boxes:
      x, y = box
      total += ((100 *y) + x)
    print('GPS Total:', total)


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

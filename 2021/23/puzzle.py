import heapq

TARGET = frozenset([
  ('A',3,3), ('A',3,2),
  ('B',5,3), ('B',5,2),
  ('C',7,3), ('C',7,2),
  ('D',9,3), ('D',9,2)
])

TARGET2 = frozenset([
  ('A',3,5), ('A',3,4), ('A',3,3), ('A',3,2),
  ('B',5,5), ('B',5,4), ('B',5,3), ('B',5,2),
  ('C',7,5), ('C',7,4), ('C',7,3), ('C',7,2),
  ('D',9,5), ('D',9,4), ('D',9,3), ('D',9,2)
])

EFFORTS = {
 'A': 1,
 'B': 10,
 'C': 100,
 'D': 1000
}

TARGET_ROOMS = {
 'A': 3,
 'B': 5,
 'C': 7,
 'D': 9
}

SPOTS = [
  (1,1), (2,1), (4,1), (6,1), (8,1), (10,1), (11,1),
  (3,2), (5,2), (7,2), (9,2),
  (3,3), (5,3), (7,3), (9,3)
]

SPOTS2 = [
  (1,1), (2,1), (4,1), (6,1), (8,1), (10,1), (11,1),
  (3,2), (5,2), (7,2), (9,2),
  (3,3), (5,3), (7,3), (9,3),
  (3,4), (5,4), (7,4), (9,4),
  (3,5), (5,5), (7,5), (9,5)
]

def find_top_of_stack(loc, occupied, maxy):
  y = maxy
  while (loc,y) in occupied:
    y -= 1
  return (loc,y)

def gen_path(start, finish):
  x1, y1 = start
  x2, y2 = finish
  path = []
  x = x1
  y = y1
  #up
  while y > 1:
    y -= 1
    path.append((x,y))
  #left/right
  if x1 < x2: #move right
    while x < x2:
      x += 1
      path.append((x,y))
  else: #left
    while x > x2:
      x -= 1
      path.append((x,y))
  #down
  while y < y2:
    y += 1
    path.append((x,y))
  return path

#Remove any moves to occupied rooms / same room
def remove_invalid(pod, options, pods, maxy):
  valid = []
  let, x, y = pod
  homecol = TARGET_ROOMS[let]
  for o in options:
    #Not valid move as does not leave room
    if o[0] == x:
      pass
    #Moving to Corridor
    elif o[1] == 1:
      valid.append(o)
    #Tring to move into a room not ours
    elif o[0] != homecol: 
      pass
    else:
      opods = set(pods_in_loc(o[0], pods))
      #Wont move to room occupied by wrong pods
      if len(opods) > 1:
        pass
      elif len(opods) == 1 and let not in opods:
        pass 
      #To and Empty room
      elif len(opods) == 0:
        #print 'Move To Empty', pod, o, maxy
        #only  move to bottom
        if o[1] != maxy:
          pass
        else:
          valid.append(o)
      else:
        valid.append(o)
  return valid

def remove_blocked(start, options, occupied):
  accessible = []
  oset = set(occupied)
  for o in options:
    #print 'Access?', start, '->', o, ':', occupied
    path = gen_path(start, o)
    collide = set(path) & oset
    if len(collide) > 0:
      #print '-- Blocked --', path
      pass
    else:
      accessible.append(o)
  return accessible

def calccost(pod, move):
  let, x1, y1 = pod
  x2, y2 = move
  effort = EFFORTS[let]
  steps = (y1-1) + abs(x2-x1) + (y2-1)
  return steps * effort

def map_states(pod, options, state):
  base = state.difference([pod])
  states = []
  for o in options:
    let = pod[0]
    cost = calccost(pod, o)
    states.append((cost, base.union([(let, o[0], o[1])])))
  return states

def transpose(pods):
  locations = {}
  for p in pods:
    let, x, y = p
    locations[(x,y)] = let
  return locations

def pods_in_loc(loc, pods):
  lets = []
  for p in pods:
    let, x, _ = p
    if x == loc:
      lets.append(let)
  return lets

class Puzzle:
  def __init__(self):
    self.target = TARGET
    self.spots = SPOTS
    self.maxy = 3
    self.pods = set()

  def process(self, text):
    self.scan_map(text)
  
  def cost(self, pod, move):
    return calccost(pod, move)

  def scan_map(self, text):
    rows = []
    for line in text.split('\n'):
      if len(line) != 0:
        row = [ch for ch in line]
        rows.append(row)
    for y in range(len(rows)):
      for x in range(len(rows[y])):
        ch = rows[y][x]
        if ch != ' ' and ch != '.' and ch != '#':
          pod = (ch, x, y)
          self.pods.add((ch, x, y))

  def gen_moves(self, pod, pods):
    let, x, y = pod
    locs = transpose(pods)
    occupied = locs.keys()
    loc = TARGET_ROOMS[let]
    opods = set(pods_in_loc(loc, pods))
    #if y == 2: #Top of Room
    if x == loc and len(opods) == 1: #home column, only my ones
      return []
    elif y > 1: #In a Room
      if locs.get((x,y-1), None) != let: #Pod above
        options = filter(lambda s: s not in occupied, self.spots)
        #Remove any moves to occupied rooms
        options = remove_invalid(pod, options, pods, self.maxy)
        #Remove any rooms inaccessible
        options = remove_blocked((x,y), options, occupied)
        return options
      else:
        return [] #We cannot move
    elif y == 1: #In Corridor
      if len(opods) == 0: #Empty Target Room
        #move to bottom of target room
        options =  [(loc, self.maxy)]
      elif len(opods) == 1:
        if let not in opods:
          return [] #Room occupied by wrong
        else:
          options = [find_top_of_stack(loc, occupied, self.maxy)]
      else: #Won't move
        return []
      #May still not be able to access
      return remove_blocked((x,y), options, occupied)
    else:
      print '====== GEN MOVES ===='
      print pod, pods
      raise 'Unimplemented'
    return []

  def unfold(self):
    self.target = TARGET2
    self.spots = SPOTS2
    self.maxy = 5
    #   Level 3 inserts
    #   #D#C#B#A#
    #   #D#B#A#C#
    newpods = set([
     ('D',3,3), ('D',3,4),
     ('C',5,3), ('B',5,4),
     ('B',7,3), ('A',7,4),
     ('A',9,3), ('C',9,4)
    ])
    for pod in self.pods:
      let, x, y = pod
      if y == 3:
        newpods.add((let, x, 5))
      else:
        newpods.add(pod)
    
    self.pods = newpods
      

  def result(self):
    #print self.pods
    self.unfold()
    #print self.pods
    #return

    pq = []
    heapq.heapify(pq)

    cheapest = {}
    state = frozenset(self.pods)
    heapq.heappush(pq, [0, state])
    while pq:
      cost, state = heapq.heappop(pq)
      if state not in cheapest:
        print 'Visiting', cost, state
        cheapest[state] = cost
        if state == self.target:
          print 'Solved', state
          return
        for pod in state:
          options = self.gen_moves(pod, state)
          #print pod, options
          mapped = map_states(pod, options, state)
          for m in mapped:
            mcost, s = m
            if frozenset(s) not in cheapest: #We never as lower cost
              #print '--', (cost + mcost, s)
              heapq.heappush(pq, [cost + mcost, frozenset(s)])

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

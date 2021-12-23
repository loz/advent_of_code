import heapq

TARGET = frozenset([
  ('A',3,3), ('A',3,2),
  ('B',5,3), ('B',5,2),
  ('C',7,3), ('C',7,2),
  ('D',9,3), ('D',9,2)
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
def remove_invalid(pod, options, pods):
  valid = []
  let, x, y = pod
  for o in options:
    if o == (x, 2): #Not valid move as in room
      pass
    else:
      opods = set(pods_in_loc(o[0], pods))
      if len(opods) == 1 and let not in opods:
          pass #Room occupied by wrong
      elif len(opods) == 0: #Empty room
        if o[1] == 2: #Can't move to top
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
    if y == 2: #Top of Room
      if locs.get((x,3), None) != let: #Above wrong pod
        options = filter(lambda s: s not in occupied, SPOTS)
        #Remove any moves to occupied rooms
        options = remove_invalid(pod, options, pods)
        #Remove any rooms inaccessible
        options = remove_blocked((x,y), options, occupied)
        return options
      else:
        return [] #We're all HOME
    elif y == 3: #Bottom of Room
      if (x,2) in occupied: #Cannot Move
        return []
      else:
        options = filter(lambda s: s not in occupied, SPOTS)
        #Remove any moves to occupied rooms / same room
        options = remove_invalid(pod, options, pods)

        #Remove any rooms inaccessible
        options = remove_blocked((x,y), options, occupied)
        return options
    else: #In Corridor
      loc = TARGET_ROOMS[let]
      pods = set(pods_in_loc(loc, pods))
      if len(pods) == 0: #Empty Target Room
        options =  [(loc, 3)]
      elif len(pods) == 1:
        if let not in pods:
          return [] #Room occupied by wrong
        else:
          options = [(loc, 2)]
      else: #Won't move
        return []
      #May still not be able to access
      return remove_blocked((x,y), options, occupied)
    return []

  def result(self):
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
        if state == TARGET:
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

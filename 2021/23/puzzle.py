TARGET = set([
  ('A',3,3), ('A',3,2),
  ('B',5,3), ('B',5,2),
  ('C',7,3), ('C',7,3),
  ('D',9,3), ('D',9,3)
])

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
      if locs[(x,3)] != let: #Above wrong pod
        options = filter(lambda s: s not in occupied, SPOTS)
        return options
      else:
        return [] #We're all HOME
    elif y == 3: #Bottom of Room
      if (x,2) in occupied: #Cannot Move
        return []
      else:
        options = filter(lambda s: s not in occupied, SPOTS)
        return options
    else: #In Corridor
      loc = TARGET_ROOMS[let]
      pods = set(pods_in_loc(loc, pods))
      if len(pods) == 0: #Empty Target Room
        return [(loc, 3)]
      elif len(pods) == 1:
        if let not in pods:
          return [] #Room occupied by wrong
        else:
          return [(loc, 2)]
      raise 'Not Implemented @Corridor'
    return []

  def result(self):
    pass

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

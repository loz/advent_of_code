import copy
import itertools

#INPUT = (0,[
#['thg', 'thc', 'plg', 'stg',],
#['plc', 'stc',],
#['prg', 'prc', 'rug', 'ruc'],
#[]
#])
#
#TARGET = (3,[
#[],
#[],
#[],
#[ 'thg', 'thc', 'plg', 'stg',
#  'plc', 'stc',
#  'prg', 'prc', 'rug', 'ruc'],
#])

INPUT = (0,[
['hyc', 'lic'],
['hyg'],
['lig'],
[]
])

TARGET = (3,[
[],
[],
[],
[ 'hyc', 'lic', 'hyg', 'lig'],
])

class Puzzle:

  def process(self, text):
    pass

  def state_hash(self, state):
    elevator, floors = state
    floors = map(lambda f: copy.copy(f), floors)
    for f in floors:
      f.sort()
    joined = map(lambda f: ','.join(f), floors)
    #fourth = joined.pop()
    #joined.sort()
    #fhash = str(elevator) + 'E:>' + fourth + ':>' + '|'.join(joined) 
    fhash = str(elevator) + 'E:>' + '|'.join(joined) 
    return fhash

  def _generate_item_moves(self, s_elevator, d_elevator, floors):
      source = floors[s_elevator]
      dest = floors[d_elevator]
      moves = []
      #1 item of either type
      for item in source:
        c_floors = copy.copy(floors)
        n_dest = dest + [item]
        n_source = filter(lambda i: i != item, source)
        c_floors[s_elevator] = n_source
        c_floors[d_elevator] = n_dest
        move = (d_elevator, c_floors)
        moves.append(move)
      gs = filter(lambda i: i.endswith('g'), source)
      cs = filter(lambda i: i.endswith('c'), source)

      #2 of gs
      gpairs = itertools.combinations(gs, 2)
      for pair in gpairs:
        c_floors = copy.copy(floors)
        n_dest = dest + list(pair)
        n_source = filter(lambda i: i not in pair, source)
        c_floors[s_elevator] = n_source
        c_floors[d_elevator] = n_dest
        move = (d_elevator, c_floors)
        moves.append(move)

      #2 of cs
      cpairs = itertools.combinations(cs, 2)
      for pair in cpairs:
        c_floors = copy.copy(floors)
        n_dest = dest + list(pair)
        n_source = filter(lambda i: i not in pair, source)
        c_floors[s_elevator] = n_source
        c_floors[d_elevator] = n_dest
        move = (d_elevator, c_floors)
        moves.append(move)
      return moves

  def _generate_lift_up(self, elevator, floors):
    if elevator < 3:
      d_elevator = elevator + 1
      return self._generate_item_moves(elevator, d_elevator, floors)
    else:
      return []

  def _generate_lift_down(self, elevator, floors):
    if elevator > 0 :
      d_elevator = elevator - 1
      return self._generate_item_moves(elevator, d_elevator, floors)
    else:
      return []

  def generate_moves(self, state):
    elevator, floors = state
    moves = []
    moves = moves + self._generate_lift_up(elevator, floors)
    moves = moves + self._generate_lift_down(elevator, floors)
    return moves

  def valid_state(self, state):
    _, floors = state
    for floor in floors:
      #see if there are any C with G not their G
      gs = filter(lambda i: i.endswith('g'), floor)
      cs = filter(lambda i: i.endswith('c'), floor)
      if len(gs) > 0: #dont care if no Gs in floor
        for chip in cs:
          pair = chip.replace(r"c", 'g')
          if pair not in gs:
            return False
    return True

  def result(self):
    visited = {}
    generated = {self.state_hash(INPUT): 0}
    tovisit = [INPUT]
    t_hash = self.state_hash(TARGET)
    print "Searching For:", t_hash
    while len(tovisit) > 0:
    #for i in range(1,100):
      visit = tovisit.pop()
      v_hash = self.state_hash(visit)
      distance = generated[v_hash]

      if v_hash == t_hash:
        print "FOUND! @", distance
        print visit
        exit()

      #print 'VISIT:', visit
      moves = self.generate_moves(visit)
      #print '>MOVES:', len(moves)
      valid = filter(lambda m: self.valid_state(m), moves)
      #valid = moves
      #print "VALID:", len(valid)
      for state in valid:
        s_hash = self.state_hash(state)
        if not generated.has_key(s_hash):
          generated[s_hash] = distance + 1
          tovisit.append(state)
      print "VISIT @", distance, "TOVISIT", len(tovisit), v_hash

if __name__ == '__main__':
  puz = Puzzle()
  #inp = open('input', 'r').read()
  #puz.process(inp)
  puz.result()

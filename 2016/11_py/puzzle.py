import copy
import itertools
import sys

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
['thg', 'thc', 'plg', 'stg','elg', 'elc', 'dig', 'dic'],
['plc', 'stc',],
['prg', 'prc', 'rug', 'ruc'],
[]
])

TARGET = (3,[
[],
[],
[],
[ 'thg', 'thc', 'plg', 'stg',
  'plc', 'stc',
  'prg', 'prc', 'rug', 'ruc',
  'elg', 'elc', 'dig', 'dic'],
])

#INPUT = (0,[
#['hyc', 'lic'],
#['hyg'],
#['lig'],
#[]
#])
#
#TARGET = (3,[
#[],
#[],
#[],
#[ 'hyc', 'lic', 'hyg', 'lig'],
#])

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
      
      #pair of G+C
      matched = []
      for chip in cs:
        gen = chip.replace('c', 'g')
        if gen in gs:
          matched.append((chip, gen))
      for pair in matched:
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

  def ordered_merge(self,states, newstates):
    if states == []:
      return newstates
    if newstates == []:
      return states
    distance, _ = newstates[0] #all new states same distance
    smin = 0
    smax = len(states)
    found = False
    cursor = 0
    while not found:
      smid = smin + ((smax-smin) / 2)
      #print smin, smax, smid, distance
      cursor, _ = states[smid]
      if cursor == distance:
        #print 'Found'
        merged = states[0:smid] + newstates + states[smid:]
        found = True
      elif cursor > distance:
        smax = smid - 1
      else:
        smin = smid + 1
      if smin >= smax:
        #print 'Not Present, Found Insert'
        merged = states[0:smin] + newstates + states[smin:]
        found = True
    #print '>>', smin, smax, smid, cursor, distance
    #print states
    #print len(states), '+', len(newstates), '=', len(states) + len(newstates)
    #merged = states[0:smid] + newstates + states[smid:]
    #print len(merged)
    #print merged
    #if len(merged) != (len(states) + len(newstates)):
    #  raise 'Bugger!'
    return merged

  def result(self):
    visited = {}
    generated = {self.state_hash(INPUT): 0}
    tovisit = [(0,INPUT)]
    tovisit_tail = []
    t_hash = self.state_hash(TARGET)
    print "Searching For:", t_hash
    while len(tovisit) > 0:
      for a in range(1,60):
        for i in range(1,1000):
          distance, visit = tovisit.pop(0)
          v_hash = self.state_hash(visit)

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
              tovisit_tail.append((distance + 1,state))
          #tovisit = self.ordered_merge(tovisit, newstates)
          if len(tovisit) == 0:
            tovisit = tovisit_tail
            tovisit_tail = []
          #print "VISIT @", distance, "TOVISIT", len(tovisit), v_hash
        print '.',
        sys.stdout.flush()
      print '@', distance

if __name__ == '__main__':
  puz = Puzzle()
  #inp = open('input', 'r').read()
  #puz.process(inp)
  puz.result()

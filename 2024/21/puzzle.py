import sys
from colorama import Fore
from itertools import combinations


DOORPAD = [
  ['7', '8', '9'],
  ['4', '5', '6'],
  ['1', '2', '3'],
  [None, '0', 'A']
]

DOORMAP = {
  '0': (1, 3),
  'A': (2, 3),
  '1': (0, 2),
  '2': (1, 2),
  '3': (2, 2),
  '4': (0, 1),
  '5': (1, 1),
  '6': (2, 1),
  '7': (0, 0),
  '8': (1, 0),
  '9': (2, 0)
}

ROBOPAD = [
  [None, '^', 'A'],
  ['<', 'v', '>']
]

ROBOMAP = {
  '^': (1, 0),
  'A': (2, 0),
  '<': (0, 1),
  'v': (1, 1),
  '>': (2, 1)
}

NBRS = [
  (-1,0, '<'),
  ( 1,0, '>'),
  (0,-1, '^'),
  (0, 1, 'v')
]


"""
   ^A
  <v>
  
  Facts: (dump_facts)
  For a robot, these are the costs of a button press
  A : A
  ^ : <A
  > : vA
  v : v<A, <vA
  < : v<<A, <v<A

  Costs for a ROBOT to make a ROBOT press these
  A :
     A => A
  ^ :
     <A => v<<A|<v<A, >^>A|>>^A
  > :
     vA => v<A|<vA, ^>A|>^A
  v :
     v<A => v<A|<vA, <A, >^>A|>>^A
     <vA => v<<A|<v<A, >A, ^>A|>^A
  < :
     v<<A => v<A|<vA, <A, A, >^>A|>>^A
     <v<A => v<<A|<v<A, >A, <A, >^>A|>>^A


"""

class Puzzle:
  def __init__(self):
    self.expansion_cache = {}
    self.calculate_doorpad_moves()
    self.calculate_robotpad_moves()

  def process(self, text):
    self.codes = []
    for line in text.split('\n'):
      self.process_line(line)

  def dump_facts(self):
    buttons = "A^>v<"
    print('For a robot, these are the costs of a button press')
    sequences = []
    for button in buttons:
      paths = self.robot_path('A', button)
      paths = [path + 'A' for path in paths]
      print(button, ':', ', '.join(paths))
      sequences.append( (button, paths) )
    print()

    print('Costs for a ROBOT to make a ROBOT press these')
    for button, paths in sequences:
      print(button, ':')
      for presses in paths:
        paths = self.robot_presses_robot(presses)
        notes = ['|'.join(p) for p in paths]
        print('  ', presses, '=>', ', '.join(notes))

  def fragment_cost(self, paths):
    cost = 0
    for bit in paths:
      cost += len(bit[0])
    return cost

  def squash_fragments(self, paths, costs):
    keys = ""
    for fragments in paths:
      best = fragments[0]
      bestcost = costs[best]
      for frag in fragments:
        fcost = costs[frag]
        if fcost < bestcost:
          best = frag
          bestcost = fcost
      keys += best
    return keys

  def select_fragments(self, paths, costs):
    selected = []
    for fragments in paths:
      best = fragments[0]
      bestcost = costs[best]
      for frag in fragments:
        fcost = costs[frag]
        if fcost < bestcost:
          best = frag
          bestcost = fcost
      selected.append(best)
    return selected

  def scan_fragments(self):
    iteration = 0
    fragments = list("A^>v<")
    known = {}
    seen = {}
    while fragments:
      print(iteration, fragments)
      newfragments = []
      for fragment in fragments:
        if fragment not in known:
          seen[fragment] = True
          paths = self.robot_presses_robot(fragment)
          known[fragment] = paths
          for bit in paths:
            for frag in bit:
              if frag not in seen:
                seen[frag] = True
                newfragments.append(frag)
      fragments = newfragments
      iteration += 1

    print('Expansion Graph:')
    #Here we have caluclated all possible recursive fragments
    #  Essentially a graph (for middle robots)
    nowcosts = {}
    for key in known:
      nowcosts[key] = self.fragment_cost(known[key])

    propcosts = {}
    for key in known:
      fragments = known[key]
      nextcosts = []
      total = 0
      for frag in fragments:
        fragcosts = [nowcosts[f] for f in frag]
        total += min(fragcosts)
        nextcosts.append( fragcosts )
      propcosts[key] = total
      #print(key, fragments, ' == ', nowcosts[key])
      #print('  ', nextcosts, ' == ', total)

    for key in known:
      fragments = known[key]
      print(key, fragments, ' == ', nowcosts[key], 'expanding to', propcosts[key])
      #nextcosts = []
      #total = 0
      #for frag in fragments:
      #  fragcosts = [propcosts[f] for f in frag]
      #  total += min(fragcosts)
      #  nextcosts.append( fragcosts )
      #print(nextcosts)

    #Make recommendations based on the EXPANSION costs
    bestmap = {}
    for key in known:
      fragments = known[key]
      best = self.select_fragments(fragments, propcosts)
      bestmap[key] = best

    print("Therefore, the best expansions are:")
    for key in known:
      print(key, '=>', bestmap[key])
    self.bestexpansions = bestmap
    self.propcosts = propcosts

  def solve_robot_path(self, a, b):
    paths = []
    shortest = float('inf')
    tovisit = [(ROBOMAP[a], [], "")]
    end = ROBOMAP[b]
    while tovisit:
      cur, path, kpath = tovisit.pop()
      if cur not in path:
        if cur == end:
          npath = path + [cur]
          if len(npath) < shortest:
            #print('Found New Shortest', kpath)
            paths = [kpath]
            shortest = len(npath)
          elif len(npath) == shortest:
            #print('Found Another Shortest', kpath)
            paths.append(kpath)
        else:
          for dx, dy, k in NBRS:
            nx, ny = cur[0] + dx, cur[1] + dy
            if nx in range(3) and ny in range(2):
              nkey = (nx, ny)
              if ROBOPAD[ny][nx] != None:
                tovisit.append( (nkey, path + [cur], kpath + k) )
    return paths

  def solve_door_path(self, a, b):
    paths = []
    shortest = float('inf')
    tovisit = [(DOORMAP[a], [], "")]
    end = DOORMAP[b]
    while tovisit:
      cur, path, kpath = tovisit.pop()
      if cur not in path:
        if cur == end:
          npath = path + [cur]
          if len(npath) < shortest:
            #print('Found New Shortest', kpath)
            paths = [kpath]
            shortest = len(npath)
          elif len(npath) == shortest:
            #print('Found Another Shortest', kpath)
            paths.append(kpath)
        else:
          for dx, dy, k in NBRS:
            nx, ny = cur[0] + dx, cur[1] + dy
            if nx in range(3) and ny in range(4):
              nkey = (nx, ny)
              if DOORPAD[ny][nx] != None:
                tovisit.append( (nkey, path + [cur], kpath + k) )
    return paths

  def calculate_doorpad_moves(self):
    self.door_paths = {}
    keys = list("A0123456789")
    for move in combinations(keys, 2):
      a, b = move
      self.door_paths[(a,b)] = self.solve_door_path(a, b)
      self.door_paths[(b,a)] = self.solve_door_path(b, a)
      self.door_paths[(a,a)] = [""]
      self.door_paths[(b,b)] = [""]

  def calculate_robotpad_moves(self):
    self.robot_paths = {}
    keys = list("A^v<>")
    for move in combinations(keys, 2):
      a, b = move
      self.robot_paths[(a,b)] = self.solve_robot_path(a, b)
      self.robot_paths[(b,a)] = self.solve_robot_path(b, a)
      self.robot_paths[(a,a)] = [""]
      self.robot_paths[(b,b)] = [""]

  def door_path(self, a, b):
    return self.door_paths[(a,b)]

  def robot_path(self, a, b):
    return self.robot_paths[(a,b)]

  def _robot_presses_robot(self, keys):
    presses = []
    last = 'A'
    for ch in keys:
      key_option = self.robot_path(last, ch)
      key_option = [k + 'A' for k in key_option]
      presses.append(key_option)
      last = ch
    return presses

  def _best_robot_presses(self, options):
    optionpresses = []
    best = float('inf')
    for opt in options:
      sets = self._robot_presses_robot(opt)
      cost = sum([len(x[0]) for x in sets])
      if cost < best:
        optionpresses = [(opt, sets)]
        best = cost
      elif cost == best:
        optionpresses.append((opt, sets))
    return optionpresses

  def _squash_options(self, options):
    # Array of options[Strings]
    #print("Squashing:", options)
    strings = [""]
    for i in range(len(options)):
      newstrings = []
      chunks = options[i]
      for string in strings:
        for chunk in chunks:
          newstrings.append(string + chunk)
      strings = newstrings
    return strings


  def robot_presses_keypad(self, code):
    last = 'A'
    presses = []
    for ch in code:
      options = self.door_path(last, ch)
      press = []
      for opt in options:
        press.append(opt + 'A')
      presses.append(press)
      last = ch
    sets = self._squash_options(presses)
    return sets

  def robot_presses_robot(self, code):
    return self._robot_presses_robot(code)

  """
    SUPER slow, as we expand all the strings :(
      The faster way seemed to be culling too soon
      TODO: Revisit
  """
  def generate_keypad_press(self, keys):
    #print("Robot Pressing Keypad (Decompression)")
    last = 'A'
    presses = []
    for ch in keys:
      options = self.door_path(last, ch)
      press = []
      for opt in options:
        press.append(opt + 'A')
      presses.append(press)
      last = ch
    sets = self._squash_options(presses)
    #print(len(sets), 'options')
    #for s in sets:
    #  print(s)

    #print("Robot Pressing Robot (Radiation)")
    presses = []
    for s in sets:
      options = self._robot_presses_robot(s)
      squashed = self._squash_options(options)
      presses += squashed
    #print(len(presses), 'options')

    #print("Robot Pressing Robot (40deg)")
    sets = presses
    presses = []
    for s in sets:
      options = self._robot_presses_robot(s)
      squashed = self._squash_options(options)
      presses += squashed
    print(len(presses), 'options')

    minlen = float('inf')
    shortests = []
    for o in presses:
      if len(o) < minlen:
        shortests = [o]
        minlen = len(o)
      elif len(o) == minlen:
        shortests.append(o)
    print(len(shortests), 'shortests', minlen)
    #print(shortests[0])
    return shortests[0]

  def alt_generate_keypad_press(self, keys):
    # Robot Presses Keypad
    # Robot Presses Robot
    # Robot Presses Robot
    # You Presses Robot (No action needed, just keys)
    print()
    print("Robot Pressing Keypad (Decompression)")
    last = 'A'
    presses = []
    for ch in keys:
      options = self.door_path(last, ch)
      press = []
      for opt in options:
        press.append(opt + 'A')
      presses.append(press)
      last = ch
    print(presses)

    
    print("Robot Pressing Robot (Radiation)")
    rad_presses = []
    for options in presses:
      optionpresses = self._best_robot_presses(options)
      rad_presses.append( optionpresses )
    for opt in rad_presses:
      print(opt)

    print("Robot Pressing Robot (-40deg)")
    deg_presses = []
    for rad_options in rad_presses:
      degrad_presses = []
      for rad, options in rad_options:
        optionpresses = []
        for opt in options:
          s_optionpresses = self._best_robot_presses(opt)
          optionpresses.append((opt, s_optionpresses))
        degrad_presses.append( (rad, optionpresses) )
      deg_presses.append( degrad_presses )

    keypress = ""
    for dopts in deg_presses:
      print('---')
      for r, ropt in dopts:
        print(r)
        rcost = 0
        #for _, opt in first:
        #  keypress += opt[0]
        
        for _, opt in ropt:
          _, first = opt[0]
          #print('FFF:', first)
          keypress += ''.join([p[0] for p in first])

          _, sets = opt[0]
          cost = sum([len(x[0]) for x in sets])
          rcost += cost
          print('  ', opt)
        print('- cost:', rcost)
    print("Me Pressing Robot:")
    print(keypress)
    return keypress

  """
    COST:
    cost of a sequence is the moves lengths required
    based on number of moves, not the inherent upstream
      cost
  """
  def sequence_cost(self, sequence):
    cost = 0
    last = 'A'
    for ch in sequence:
      moves = self.robot_path(last, ch)
      cost += len(moves[0])
      last = ch
    return cost

  def process_line(self, line):
    if line != '':
      self.codes.append(line)

  def _expand_best_chunk(self, presses):
    result = ""
    chunks = presses.split('A')
    for chunk in chunks:
      if chunk in self.expansion_cache:
        result += self.expansion_cache[chunk] + 'A'
      else:
        value = self.robot_presses_robot(chunk + 'A')
        flatten = self._squash_options(value)
        bestcost = float('inf')
        best = None
        for f in flatten:
          fcost = self.sequence_cost(f)
          if fcost < bestcost:
            bestcost = fcost
            best = f
          #print('(', chunk, ') ?=', f, ':', len(f), self.sequence_cost(f))
        #print(flatten)
        self.expansion_cache[chunk] = best
        result += best + 'A'
      #print('-'*10)
    return result
  
  def _expand_all_chunks(self, presses):
    results = [""]

    chunks = presses.split('A')
    #print('Chunks:', chunks)
    for chunk in chunks:
      items = []
      if chunk in self.expansion_cache:
        items = self.expansion_cache[chunk]
      else:
        print('.', end='', flush=True)
        value = self.robot_presses_robot(chunk + 'A')
        flatten = self._squash_options(value)
        chunkcache = []
        for f in flatten:
          chunkcache.append(f)
        self.expansion_cache[chunk] = chunkcache
        items = chunkcache

      #print('Items', items)
      newresults = []
      for result in results:
        for item in items:
          newresults.append(result + item + 'A')
      #print('---')
      #print(newresults)
      results = newresults
    return results

  def _expand_chunks(self, presses, each=False):
    if each:
      return self._expand_all_chunks(presses)
    else:
      return self._expand_best_chunk(presses)

  def count_best(self, keys, depth):
    self.seen_best = {}
    options = self.robot_presses_robot(keys)
    fragments = self.select_fragments(options, self.propcosts)
    return self._count_best(fragments, depth-1)

  def _count_best(self, fragments, depth):
    if depth == 0:
      return len(''.join(fragments))

    cost = 0
    for frag in fragments:
      if (frag, depth) in self.seen_best:
        cost += self.seen_best[(frag, depth)]
      else:
        newfragments = self.bestexpansions[frag]
        fcost = self._count_best(newfragments, depth-1)
        self.seen_best[(frag,depth)] = fcost
        cost += fcost
    return cost

  def expand_best(self, keys, depth):
    #print("Expand:", keys, 'For', depth)
    #Expand the first set
    options = self.robot_presses_robot(keys)
    #print('----')
    #results = self._squash_options(options)
    #for r in results:
    #  print(' ', r)
    #print('----')
    fragments = self.select_fragments(options, self.propcosts)
    test = ''.join(fragments)
    #print('Expanded:', test, test in results)
    #print('----')

    for i in range(depth-1):
      print(i, ',', end='', flush=True)
      #print(i, fragments)
      options = self.robot_presses_robot(''.join(fragments))
      #print('  ----')
      #results = self._squash_options(options)
      #for r in results:
      #  print('   ', r)
      #print('  ----')
      newfragments = []
      for frag in fragments:
        newfragments += self.bestexpansions[frag]
      fragments = newfragments

    #test = ''.join(fragments)
    #print('Expanded:', test, test in results)
    #print('----')
    print()
    return ''.join(fragments)
  
  def _expand(self, presses, depth, bests, returns, debug):
    if depth == 0:
      return presses

    if (presses, depth) in self.expansion_cache:
      #print('.', end='', flush=True)
      return self.expansion_cache[(presses, depth)]

    print('.', end='', flush=True)
    result = ""
    last = "A"
    for ch in presses:
      if ch == last:
        expanded = "A"
      else:
        if ch == 'A':
          move = returns[last] + bests[ch]
        else:
          moves = self.robot_path(last, ch) 
          #print(moves)
          move = moves[0] #TODO: Find BEST based on repetition
          move = move + 'A'
        expanded = move
      if debug:
        result += self._expand(expanded, depth-1, bests, returns, debug) + '[' + ch + '] '
      else:
        result += self._expand(expanded, depth-1, bests, returns, debug)

      last = ch
    self.expansion_cache[(presses, depth)] = result
    return result

  def result(self):
    self.result2()

  def result2(self):
    self.scan_fragments()
    
    endrobots = []
    for code in self.codes:
      endrobots.append( (code, self.robot_presses_keypad(code)) )

    print("This is what the end robot must do")
    for i in endrobots:
      print(i)

    depth = 25 #intermediary robots between ME and last robot
    depth = 2 #intermediary robots between ME and last robot
    #depth = 25 #intermediary robots between ME and last robot

    #print("Intermediary Robots Act best as follows:")
    #for key in bests:
    #  print(key, ':>', bests[key], 'returning', returns[key])

    
    results = []
    print("Expanding Last Robot moves")
    for i in endrobots:
      code, options = i
      choices = []
      for opt in options:
        #best = self.expand_best(opt, depth)
        best = self.count_best(opt, depth)
        choices.append(best)
      best = choices[0]
      for c in choices:
        if c < best:
          best = c
      results.append((code, best))

    total = 0
    for code, moves in results:
      num = int(code.replace('A', ''))
      complexity = moves * num
      total += complexity
      print(code, moves, ' :>', complexity)
      #print(code, moves, len(moves), ' :>', complexity)
    print('Total Complexity:', total)
      

  def result1(self):
    #keys = list("A0123456789")
    #bests = {}
    #for key in keys:
    #  bests[key] = self.generate_keypad_press(key)
    
    #for k in bests:
    #  print(k, ':>', bests[k])

    total = 0
    for code in self.codes:
      #  presses = ""
      #  for ch in code:
      #    presses += bests[ch] + '   '
      #  print(code, presses, len(presses))
      presses = self.generate_keypad_press(code)
      num = int(code.replace('A', ''))
      complexity = len(presses) * num
      total += complexity
      print(code, presses, len(presses), num, complexity)
    print('Total Complexity:', total)


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

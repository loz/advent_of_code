import sys
from colorama import Fore
from collections import deque

class Machine:
  def __init__(self, line):
    hunks = line.split(' ')
    x = hunks.pop(0)
    self.diagram = x[1:-1]
    j = hunks.pop()
    b = []
    for h in hunks:
      ns = h[1:-1]
      ns = ns.split(',')
      ns = list(map(int, ns))
      b.append(ns)
    self.buttons = b
    js = j[1:-1]
    js = js.split(',')
    js = list(map(int, js))
    self.joltages = js

  def shortest_press(self):
    lights = len(self.diagram) * '.'
    tovisit = deque()
    visited = {}
    for b in range(len(self.buttons)):
      tovisit.append(([b], lights))

    while tovisit:
      cur = tovisit.popleft()
      (buttons, lights) = cur
      b = buttons[-1]
      nlights = self.press_button(b, lights)
      #print('V:', buttons, '@', lights, '->', nlights, 'vs', self.diagram)
      if nlights == self.diagram:
        press= list(map(lambda x: self.buttons[x], buttons)) 
        #print('Press:', press, '=>', nlights)
        return press
      else:
        for b in range(len(self.buttons)):
          tovisit.append((buttons + [b], nlights))

  def xfind_candidates(self, jpos, joltages):
    target = self.joltages[jpos]
    #print(jpos, joltages, 'v', target)
    if joltages[jpos] < target:
      options = []
      for b in range(len(self.buttons)):
        btns = self.buttons[b]
        if jpos in btns:
          options.append(b)
      return options
    else:
      return []

  def find_candidates(self, jpos, joltages):
    target = self.joltages[jpos]
    if joltages[jpos] < target:
      options = []
      for b in range(len(self.buttons)):
        btns = self.buttons[b]
        if jpos in btns:
          # Check this button won't over-press anything
          valid = True
          helpful_count = 0
          for pos in btns:
            if joltages[pos] >= self.joltages[pos]:
              valid = False
              break
            if joltages[pos] < self.joltages[pos]:
              helpful_count += 1
          
          if valid:
            options.append((helpful_count, b))
      
      # Sort by most helpful positions first (greedy)
      options.sort(reverse=True)
      return [b for (_, b) in options]
    else:
      return [] 

  def shortest_press_with_joltage(self):
    tovisit = deque()
    seen = {}
    joltages = self.calc_joltage([])
    candidates = self.find_candidates(0, joltages)
    for c in candidates:
      tovisit.append((c, 0, joltages))

    while tovisit:
      cur = tovisit.popleft()
      (button, presses, joltages) = cur
      seen[tuple(joltages)] = presses
      jolts = self.press_button_with_jolts(button, joltages)
      if self.meets_joltage(jolts):
        return presses + 1
      elif tuple(jolts) not in seen:
        first = self.first_unmet_joltage(jolts)
        if first != -1:
          candidates = self.find_candidates(first, jolts)
          for c in candidates:
            tovisit.append((c, presses + 1, jolts))

  def calc_joltage(self, buttons):
    joltages = [0] * len(self.joltages)
    for b in buttons:
      ps = self.buttons[b]
      for p in ps:
        joltages[p] += 1
    return joltages

  def first_unmet_joltage(self, joltage):
    first = -1
    for x in range(len(self.joltages)):
      if joltage[x] > self.joltages[x]:
        return -1
      elif joltage[x] < self.joltages[x]:
        if first == -1:
          first = x
    return first

  def meets_joltage(self, joltage):
    for x in range(len(self.joltages)):
      if joltage[x] != self.joltages[x]:
        return False
    return True

  def press_button(self, b, lights):
    places = self.buttons[b]
    nlights = ''
    for x in range(len(lights)):
      ch = lights[x]
      if x in places:
        if lights[x] == '.':
          nlights += '#'
        else:
          nlights += '.'
      else:
        nlights += ch
    return nlights

  def press_button_with_jolts(self, b, jolts):
    places = self.buttons[b]
    njolts = []
    for x in range(len(self.joltages)):
      if x in places:
        njolts.append(jolts[x] + 1)
      else:
        njolts .append(jolts[x])
    return njolts
    
class Puzzle:

  def __init__(self):
    self.machines = []

  def process(self, text):
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      self.machines.append(Machine(line))

  def result1(self):
    total = 0
    for m in self.machines:
      press = m.shortest_press()
      print(m.diagram, len(press))
      total += len(press)
    print('Total:', total)

  def result(self):
    total = 0
    for m in self.machines:
      print(m.joltages, '...', end='', flush=True)
      count = m.shortest_press_with_joltage()
      print(count)
      total += count
    print('Total:', total)


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

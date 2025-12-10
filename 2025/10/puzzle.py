import sys
from colorama import Fore
from collections import deque
import numpy as np
from pulp import LpMinimize, LpProblem, LpVariable, lpSum, PULP_CBC_CMD


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

  def shortest_press_with_joltage(self):
    # Step 1: Create the problem - we want to MINIMIZE something
    prob = LpProblem("ButtonPresses", LpMinimize)
    # Step 2: Create variables - one for each button
    # We need non-negative integers (can't press -5 times or 2.7 times)
    button_vars = []
    for i in range(len(self.buttons)):
        var = LpVariable(f"button_{i}", lowBound=0, cat='Integer')
        button_vars.append(var)
    # Step 3: Set the objective - minimize total presses
    # This is the sum: button_0 + button_1 + button_2 + ... + button_n
    prob += lpSum(button_vars)

    # Step 4: Add constraints - ensure final joltages match target
    for j in range(len(self.joltages)):
      #print(j, self.buttons)
      impacts = []
      for b in range(len(self.buttons)):
        positions = self.buttons[b]
        if(j in positions):
          impacts.append(button_vars[b])
      #print('Impacts for position', j, ':', impacts)
      prob += lpSum(impacts) == self.joltages[j];

    #print(prob);
    # Step 5: Solve the problem
    prob.solve(PULP_CBC_CMD(msg=0))  # msg=0 suppresses solver output

    # Step 6: Extract the solution
    # Check if we found a valid solution
    if prob.status == 1:  # 1 means "Optimal solution found"
        total_presses = sum(var.varValue for var in button_vars)
        return int(total_presses)
    else:
        return None  # No solution found

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

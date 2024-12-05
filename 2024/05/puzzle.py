import sys
from colorama import Fore

class Puzzle:

  def process(self, text):
    self.rules = []
    self.orders = []
    rules, orders = text.split('\n\n')

    for line in rules.split('\n'):
      self.process_rule(line)

    for line in orders.split('\n'):
      self.process_order(line)
    
    self.calulate_dependencies()

  def calulate_dependencies(self):
    self.dependencies = {}
    for rule in self.rules:
      prev, suc = rule
      rules = self.dependencies.get(suc, [])
      rules.append(prev)
      self.dependencies[suc] = rules

  def process_rule(self, line):
    if line != '':
      left, right = line.split('|')
      self.rules.append((int(left), int(right)))

  def process_order(self, line):
    if line != '':
      items = line.split(',')
      self.orders.append([int(n) for n in items])

  def valid_order(self, order):
    #If there's a dependency in this list
    # have we seen it
    seen = {}
    required = {}
    for item in order:
       required[item] = True
    for item in order:
       deps = self.dependencies.get(item, [])
       for dep in deps:
         if required.get(dep, False) and not seen.get(dep, False):
           return False
       seen[item] = True
    return True

  def swap_pages(self, order):
    didSwap = False
    seen = {}
    required = {}
    swaps = []
    for item in order:
       required[item] = True
    for item in order:
       deps = self.dependencies.get(item, [])
       for dep in deps:
         if required.get(dep, False) and not seen.get(dep, False):
           swaps.append((item, dep))
       seen[item] = True

    while swaps:
      didSwap = True
      a, b = swaps.pop()
      idx1 = order.index(a)
      idx2 = order.index(b)
      #print(a, b, idx1, idx2)
      tmp = order[idx2]
      order[idx2] = order[idx1]
      order[idx1] = tmp

    return order, didSwap

  def sort_order(self, order):
    order, didSwap = self.swap_pages(order)
    while didSwap:
       order, didSwap = self.swap_pages(order)
    return order

  def result(self):
    total = 0
    for order in self.orders:
      v = self.valid_order(order)
      if not v:
         order = self.sort_order(order)
         print(order, Fore.GREEN + 'Fixed' + Fore.RESET)
         mid = int(len(order) / 2)
         total += order[mid]
      else:
         print(order)
    print('Total:', total)

  def result1(self):
    total = 0
    for order in self.orders:
      v = self.valid_order(order)
      if v:
         print(order, Fore.GREEN + 'Valid' + Fore.RESET)
         mid = int(len(order) / 2)
         total += order[mid]
      else:
         print(order)
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

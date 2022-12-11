import sys

class Monkey:
  def __init__(self):
    self.items = []
    self.inspection_count = 0
    self.targets = (None, None)

  def dump(self):
    print 'Monkey', self.id, ':', self.items

  def give(self, item):
    self.items.append(item)

  def play(self, monkeys):
    deflate = 1
    for monkey in monkeys:
      deflate *= monkey.divisor

    self.inspection_count += len(self.items)
    newitems = [i for i in self.items]
    for item in newitems:
      arg1, op, arg2 = self.operation
      if arg2 == 'old':
        arg2 = item

      if op == '+':
        newval = item + arg2
      elif op == '*':
        newval = item * arg2

      #Decrease worry
      #newval = newval / 3
      
      newval = newval % deflate

      t, f = self.targets
      if newval % self.divisor == 0:
        monkeys[t].give(newval)
      else:
        monkeys[f].give(newval)
    self.items = []

class Puzzle:

  def process(self, text):
    self.monkeys = []
    chunks = text.split('Monkey ')
    for chunk in chunks:
      self.process_chunk(chunk)

  def process_chunk(self, chunk):
    if chunk != '':
      monkey = Monkey()
      for line in chunk.split('\n'):
        self.process_line(line, monkey)
      self.monkeys.append(monkey)

  def process_line(self, line, monkey):
    if line != '':
      line = line.strip()
      if line.startswith('Starting items:'):
        nline = line.replace('Starting items: ', '')
        items = nline.split(', ')
        for item in items:
          monkey.give(int(item))
      elif line.startswith('Operation'):
        nline = line.replace('Operation: new = ', '')
        arg1, op, arg2 = nline.split(' ')
        if arg2 != 'old':
          arg2 = int(arg2)
        monkey.operation = (arg1, op, arg2)
      elif line.startswith('Test'):
        nline = line.replace('Test: divisible by ', '')
        monkey.divisor = int(nline)
      elif line.startswith('If true'):
        nline = line.replace('If true: throw to monkey ', '')
        target = int(nline)
        t, f = monkey.targets
        monkey.targets = (target, f)
      elif line.startswith('If false'):
        nline = line.replace('If false: throw to monkey ', '')
        target = int(nline)
        t, f = monkey.targets
        monkey.targets = (t, target)
      else:
        nline = line.replace(':', '')
        idx = int(nline)
        monkey.id = idx
      pass

  def result(self):
    counter = 0
    chunk = 1000
    for r in range(10):
      for c in range(chunk):
        for monkey in self.monkeys:
          monkey.play(self.monkeys)

        #for monkey in self.monkeys:
        #  monkey.dump()
      print '=' * 40
      counter += chunk
      print 'Round', counter
      for monkey in self.monkeys:
        print 'Monkey', monkey.id, 'inspected', monkey.inspection_count
    for monkey in self.monkeys:
      monkey.dump()



if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

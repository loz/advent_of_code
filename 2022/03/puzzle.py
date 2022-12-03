class Puzzle:
  def __init__(self):
    self.priorities = {}
    for l in range(26):
      letter = chr(ord('a')+l)
      self.priorities[letter] = l+1
    for l in range(26):
      letter = chr(ord('A')+l)
      self.priorities[letter] = l+27

  def process(self, text):
    self.bags = []
    self.groups = [[]]
    self.numgroups = 0
    for line in text.split('\n'):
      self.process_line(line)
    self.groups.pop()

  def process_line(self, line):
    if line != '':
      size = len(line)
      half = size / 2
      left = [i for i in line[0:half]]
      right = [i for i in line[half:size]]
      bag = (left, right)
      self.bags.append(bag)
      self.groups[self.numgroups].append(bag)
      if len(self.groups[self.numgroups]) == 3:
        self.numgroups += 1
        self.groups.append([])

  def badge(self, group):
    b1 = group[0]
    b2 = group[1]
    b3 = group[2]
    b1 = set(b1[0] + b1[1])
    b2 = set(b2[0] + b2[1])
    b3 = set(b3[0] + b3[1])
    possible = b1.intersection(b2)
    badge = possible.intersection(b3)
    return badge.pop()

  def shared(self, bag):
    left, right = bag
    common = [c for c in left if c in right]
    return common

  def priority(self, items):
    total = 0
    for i in items:
      total += self.priorities[i]
    return total

  def group(self, n):
    return self.groups[n]

  def result(self):
    total = 0
    for b in self.bags:
      shared = set(self.shared(b))
      score = self.priority(shared)
      total += score
      print b, shared, score
    print 'Total', total

  def result2(self):
    total = 0
    for g in self.groups:
      print g
      badge = self.badge(g)
      print badge
      score = self.priority([badge])
      total += score
    print 'Total', total


if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result2()

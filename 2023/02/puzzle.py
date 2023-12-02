import sys

class Game:
  def __init__(self, line):
    left, right = line.split(': ')
    self.id = int(left.replace('Game ', ''))
    self.parse_rounds(right)

  def parse_rounds(self, right):
    rounds = right.split('; ')
    self.rounds = []
    for r in rounds:
      sets = r.split(', ')
      rset = []
      for s in sets:
        n, colour = s.split(' ')
        rset.append((colour, int(n)))
      self.rounds.append(rset)

  def possible(self, contents):
    for rset in self.rounds:
      totals = {}
      for colour, count in rset:
        totals[colour] = totals.get(colour,0) + count
      for colour in totals:
        if contents[colour] < totals[colour]:
          return False
    return True

  def mincubes(self):
    minsets = {}
    for rset in self.rounds:
      totals = {}
      for colour, count in rset:
        totals[colour] = totals.get(colour,0) + count
      for colour in totals:
        if minsets.get(colour, 0) < totals[colour]:
          minsets[colour] = totals[colour]
    return minsets


class Puzzle:

  def process(self, text):
    self.games = []
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      game = Game(line)
      self.games.append(game)

  def result(self):
    total = 0
    for g in self.games:
      m = g.mincubes()
      p = 1
      for colour in m:
        p = p * m[colour]
      print(g.id, m, p)
      total += p
    print('Total', total)

  def result1(self):
    bag = {'red':12, 'green':13, 'blue':14}
    total = 0
    for g in self.games:
      p = g.possible(bag)
      print(g.id, p)
      if p:
        total += g.id
    print('Total', total)



if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

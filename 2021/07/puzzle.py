import math
class Puzzle:

  def process(self, text):
    lines = text.rstrip().split(',')
    self.crabs = map(lambda x: int(x), lines)

  def fuel_cost(self, loc):
    cost = 0
    for crab in self.crabs:
      dist = abs(crab - loc)
      cost += (dist * (dist+1))/2
    return cost

  def cheapest(self):
    upper = max(self.crabs)
    cheapest = upper
    cheapcost = 9999999999

    for loc in range(0, upper+1):
      cost = self.fuel_cost(loc)
      if cost < cheapcost:
        cheapest = loc * 1
        cheapcost = cost
      print loc, cost
    return (cheapest, cheapcost)
    

  def result(self):
    print 'Cheapest', self.cheapest()

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

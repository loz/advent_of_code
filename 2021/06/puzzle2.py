class Puzzle:

  def process(self, text):
    text=text.rstrip()
    self.known_growths = {}
    nums = text.split(',')
    self.state = map(lambda x: int(x), nums)

  def tick(self):
    new_state = []
    new_fish = []
    for fish in self.state:
      if fish == 0:
        new_state.append(6)
        new_fish.append(8)
      else:
        new_state.append(fish -1)
    self.state = new_state + new_fish

  def to_str(self):
    return ','.join(map(lambda n: str(n), self.state))

  def result(self):
    #print 'Initial state:', self.to_str()
    #for day in range(1,80+1):
    #  self.tick()
    #  #print 'After', day, 'days:', self.to_str()
    #print 'Total Fish:', len(self.state)
    growth = 0
    for fish in self.state:
      print fish
      growth += self.calculate_growth(fish, 256)
    print 'Total Growth', growth


  # All 0, 1, 2, 3, 4, 5, 6, 7, 8 grow exactly the same
  def calculate_growth(self, timer, days, nest=''):
    if timer not in self.known_growths:
      self.known_growths[timer] = self._calculate_growth(timer, days)
      print self.known_growths[timer]
    return self.known_growths[timer]

  def _calculate_growth(self, timer, days):
    growth = 1 #self
    spawnat = (days - timer)
    newfish = spawnat / 7
    remains = spawnat % 7
    if spawnat <= 0:
      return growth
    if remains != 0:
      newfish += 1
    print 'S:', spawnat, 'N:', newfish
    for fish in range(newfish):
      growth += self._calculate_growth(8, spawnat-1-(7*fish))
    return growth

#  def _calculate_growth(self, timer, days, nest=''):
#    growth = 1 #self
#    spawnat = (days - timer)
#    newfish = spawnat / 7
#    remains = spawnat % 7
#    if spawnat <= 0:
#      return growth
#    if remains != 0:
#      newfish += 1
#    #print nest, 'S:', spawnat, 'N:', newfish
#    for fish in range(newfish):
#      growth += self._calculate_growth(8, spawnat-1-(7*fish), nest + '.')
#    return growth

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

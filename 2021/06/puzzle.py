class Puzzle:

  def process(self, text):
    text=text.rstrip()
    print text
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
    print 'Initial state:', self.to_str()
    for day in range(1,80+1):
      self.tick()
      print 'After', day, 'days:', self.to_str()
    print 'Total Fish:', len(self.state)

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

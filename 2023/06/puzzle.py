import sys

class Puzzle:

  def process(self, text):
    self.records = []
    lines = text.split('\n')
    times = lines[0]
    distances = lines[1]
    self.process_records(times, distances)

  def process_records(self, times, distances):
    times = self.mapvalues(times)
    distances = self.mapvalues(distances)
    self.records = list(zip(times, distances))

  def mapvalues(self, text):
    _, tv = text.split(':')
    values = []
    for v in tv.split(' '):
      if v != '':
        values.append(int(v))
    return values
  
  def calculate_distance(self, press, limit):
    return (press * (limit-press))

  def wincount(self, limit, record):
    pass

  def brute_wincount(self, limit, record):
    wins = 0
    for h in range(limit):
      bd = self.calculate_distance(h, limit)
      win = bd > record
      if win:
        wins += 1
      #print(':', h, bd, win)
    return wins

  def result(self):
    self.result1()

  def result1(self):
    score = 1
    for r in self.records:
      print('Race', r)
      t, rec = r
      wins = self.brute_wincount(t, rec)
      score *= wins
      print(wins, 'Wins')
    print('Win Multiplier', score)



if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

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

  def minsearch(self, limit, record):
    lower = 0
    upper = limit/2
    while lower < upper:
      mid = int((lower + upper) / 2)
      score = self.calculate_distance(mid, limit)
      win = score > record
      #print('Srch', lower, upper, score)
      if win:
        upper = mid-1
      else:
        lower = mid+1
    score = self.calculate_distance(lower, limit)
    if score > record:
      return lower
    else:
      return lower+1
    return lower

  def maxsearch(self, limit, record):
    lower = limit/2
    upper = limit
    while lower < upper:
      mid = int((lower + upper) / 2)
      score = self.calculate_distance(mid, limit)
      win = score > record
      #print('Srch', lower, upper, score)
      if win:
        lower = mid+1
      else:
        upper = mid-1
    score = self.calculate_distance(upper, limit)
    if score > record:
      return upper
    else:
      return upper-1

  def wincount(self, limit, record):
    #Binsearch lowest win combination
    lower = self.minsearch(limit, record)
    #Binsearch highest combination
    upper = self.maxsearch(limit, record)
    #Range is answer
    #print('Range', lower, upper)
    return upper - lower + 1

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
    self.result2()

  def result2(self):
    t, rec = self.records.pop(0)
    t = str(t)
    rec = str(rec)
    while(self.records):
      nt, nrec = self.records.pop(0)
      t = t + str(nt)
      rec = rec + str(nrec)
    print(t, rec)
    t = int(t)
    rec = int(rec)
    print('Wins', self.wincount(t, rec))

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

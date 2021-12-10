class Puzzle:

  def process(self, text):
    self.lines = text.split('\n')


  def check(self, string):
    pairing = {
      '[' : ']',
      '(' : ')',
      '<' : '>',
      '{' : '}'
    }
    scores = {
      ')' : 3,
      ']' : 57,
      '}' : 1197,
      '>' : 25137
    }
    points = {
      ')' : 1,
      ']' : 2,
      '}' : 3,
      '>' : 4
    }
    tomatch = []
    for ch in string:
      if ch in ['[', '(', '<', '{']:
        tomatch.append(ch)
      else:
        op = tomatch.pop()
        if ch != pairing[op]:
          return scores[ch], 0
    autoscore = 0
    while len(tomatch) > 0:
      ch = tomatch.pop()
      op = pairing[ch]
      autoscore *= 5
      autoscore += points[op]
    return 0, autoscore

  def result1(self):
    total = 0
    for line in self.lines:
      score = self.check(line)
      total += score
      print line, score
    print 'Total', total

  def result(self):
    scores = []
    for line in self.lines:
      score, autoscore = self.check(line)
      if score == 0:
        print line, autoscore
        scores.append(autoscore)
    scores.sort()
    print 'Middle', scores[len(scores)/2]

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

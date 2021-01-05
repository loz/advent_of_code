class Puzzle:

  def process(self, text):
    streams = []
    lines = text.split('\n')
    for line in lines:
      if line.strip() != '':
        streams.append(line)
    self.streams = streams

  def _consume_garbage(self, chars):
    if len(chars) == 0:
      return chars, 0
    count = 0
    ch = chars.pop(0)
    while ch != '>' and len(chars) > 0:
      count += 1
      if ch == '!':
        count -= 1
        chars.pop(0)
        ch = '.snip.'
      ch = chars.pop(0)
    return (chars, count)

  def _consume_to(self, target, chars, depth):
    groups = 0
    score = 0
    garbage = 0
    if len(chars) == 0:
      return (chars, 0, 0, 0)
    ch = chars.pop(0)
    while ch != target and len(chars) > 0:
      if ch == '{':
        chars, ngroups, nscore, gscore = self._consume_to('}', chars, depth + 1)
        groups += ngroups
        score += nscore
        garbage += gscore
      elif ch == '<':
        chars, gcount = self._consume_garbage(chars)
        garbage += gcount
      if len(chars) > 0:
        ch = chars.pop(0)
    if ch == target:
      groups += 1
      score += depth
    return (chars, groups, score, garbage)

  def count_group(self, string):
    count, _, _ = self._score_group(string)
    return count

  def score_group(self, string):
    _, score, _ = self._score_group(string)
    return score

  def count_garbage(self, string):
    _, _, count = self._score_group(string)
    return count

  def _score_group(self, string):
    groups = 0
    score = 0
    garbage = 0
    chars = [ch for ch in string]
    while len(chars) > 0:
      ch = chars.pop(0)
      if ch == '{':
        chars, ngroups, nscore, gscore = self._consume_to('}', chars, 1)
        groups += ngroups
        score += nscore
        garbage += gscore
      elif ch == '<':
        chars, gcount = self._consume_garbage(chars)
        garbage += gcount
    return (groups, score, garbage)

  def result(self):
    total = 0
    gtotal = 0
    for stream in self.streams:
      score = self.score_group(stream)
      garbage = self.count_garbage(stream)
      print stream, score, garbage
      total += score
      gtotal += garbage
    print 'Total Scores', total
    print 'Total Garbage', gtotal

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

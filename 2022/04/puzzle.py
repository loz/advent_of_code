class Puzzle:

  def process(self, text):
    self.pairs = []
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      left, right = line.split(',')
      left = self.parse_range(left)
      right = self.parse_range(right)
      self.pairs.append((left, right))

  def parse_range(self, token):
    start, end = token.split('-')
    start = int(start)
    end = int(end)
    return (start, end)

  def contains(self, left, right):
    ls, le = left
    rs, re = right
    if ls <= rs and le >= re:
      return True
    elif rs <= ls and re >= le:
      return True

    return False

  def overlaps(self, left, right):
    ls, le = left
    rs, re = right
    if ls <= rs and le >= re:
      return True
    elif rs <= ls and re >= le:
      return True
    elif ls <= rs and le >= rs:
      return True
    elif rs <= ls and re >= ls:
      return True

    return False

  def result(self):
    count = 0
    for pair in self.pairs:
      match = self.contains(pair[0], pair[1])
      if match:
        count +=1
      print pair, match
    print "Containing", count

  def result2(self):
    count = 0
    for pair in self.pairs:
      match = self.overlaps(pair[0], pair[1])
      if match:
        count +=1
      print pair, match
    print "Overlapping", count



if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result2()

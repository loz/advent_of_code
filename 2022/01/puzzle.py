class Puzzle:

  def process(self, text):
    self.calories = [0]
    self.current = 0
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line == '':
      self.current += 1
      self.calories.append(0)
    else:
      cal = int(line)
      self.calories[self.current] += cal

  def result(self):
    print 'Total Elves', len(self.calories)
    print 'Largest', max(self.calories)
    self.calories.sort(reverse = True)
    top3 = self.calories[0:3]
    print 'Top 3', top3, sum(top3)


if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

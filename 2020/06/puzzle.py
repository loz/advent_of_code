class Puzzle:

  def process(self, text):
    lines = text.split('\n')
    groups = []
    common = []
    group = []
    for line in lines:
      if line.strip() == '':
        groups.append(group)
        common.append(self.calc_common(group))
        group = []
      else:
        group.append(list(line))
    self.groups = groups
    self.common_answers = common

  def calc_common(self, grp):
    common = grp[0]
    for member in grp:
      newcommon = filter(lambda x: x in common, member)
      common = newcommon
    return len(common)

  def let_freq(self, grp):
    freq = {}
    for answers in grp:
      for ch in answers:
        if not freq.has_key(ch):
          freq[ch] = 0
        freq[ch] = freq[ch] + 1
    return freq

  def result(self):
    total = 0
    for group in self.groups:
      freq = self.let_freq(group)
      print len(freq.keys())
      total = total + len(freq.keys())
    print "Total:", total
    total = 0
    for common in self.common_answers:
      print common
      total = total + common
    print "Total Shared:", total

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

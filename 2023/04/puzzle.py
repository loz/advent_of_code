import sys

class Puzzle:

  def process(self, text):
    self.cards = []
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      self.cards.append(self.parse_card(line))

  def parse_card(self, line):
    cd, rest = line.split(': ')
    cd = cd.replace('Card ', '')
    cd = int(cd)
    lhs, rhs = rest.split(' | ')
    return (cd, self.process_numbers(lhs), self.process_numbers(rhs))

  def process_numbers(self, text):
    ns_txt = text.split(' ')
    ns = []
    for nt in ns_txt:
      if nt != '':
        ns.append(int(nt))
    return ns

  def score(self, card):
    win = self.wins(card)
    if win  == 0:
      return 0
    return pow(2,(win-1))

  def wins(self, card):
    count = 0
    i, win, have = card
    for c in have:
      if c in win:
        count = count + 1
    if count == 0:
      return 0
    return count

  def winnings(self, card):
    i, win, have = card
    sc = self.wins(card)
    if sc == 0:
      return []
    else:
      won = []
      for n in range(sc):
        if i+n < len(self.cards):
          won.append(self.cards[i+n])
      return won
        

  def result1(self):
    total = 0
    for card in self.cards:
      sc = self.score(card)
      total = total + sc
      print(card, sc)
    print('Total', total)

  def count_winnings(self, card, indent=' '):
    if self.seen.get(card[0], False):
      return self.seen[card[0]]
    total = 1
    wins = self.winnings(card)
    print('Wins', len(wins))
    for win in wins:
      print(indent, win)
      total = total + self.count_winnings(win, indent + ' ')
    self.seen[card[0]] = total
    return total

  def result(self):
    self.seen = {}
    total = 0
    for card in self.cards:
      print(card)
      total = total + self.count_winnings(card)
    print('Total', total)


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

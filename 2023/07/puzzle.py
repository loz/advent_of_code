import sys
import functools

ORDER = "23456789TJQKA"

class Puzzle:

  def process(self, text):
    self.turns = []
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      cards, bid = line.split(' ')
      bid = int(bid)
      self.turns.append((cards, bid))

  def score(self, cards):
    sets = {}
    for ch in cards:
      cur = sets.get(ch, 0)
      cur += 1
      sets[ch] = cur
    diffs = list(sets.keys())
    counts = list(sets.values())
    #print(sets, diffs, counts, len(diffs))
    if len(diffs) == 1: #5 of a kind
      return 7
    elif len(diffs) == 2: #4 of a kind or FH
      if 4 in counts:
        return 6
      else:
        return 5 #FH
    elif len(diffs) == 3: #4 of a kind or 2Pair
      if 3 in counts: #3 of kinds
        return 4
      else:
        return 3 #2p
    elif len(diffs) == 4: #1 pair
      return 2
    return 1

  def cmp_hand(a, b):
    aval = [ORDER.index(ch) for ch in a]
    bval = [ORDER.index(ch) for ch in b]
    #print('Cmp', aval, bval)
    while(aval):
      ai = aval.pop(0)
      bi = bval.pop(0)
      if ai != bi:
        if ai > bi:
          return 1
        else:
          return -1

    return 0

  def result(self):
    self.result1()

  def cmp_ranked(a, b):
    if a[1] == b[1]: #Same Rank
      return Puzzle.cmp_hand(a[0], b[0])
    elif a[1] > b[1]:
      return 1
    else:
      return -1


  def result1(self):
    #pre-rank
    ranked = []
    for hand, bid in self.turns:
      ra = (hand, self.score(hand), bid)
      print(ra)
      ranked.append(ra)
    print('Sorting:')
    rsorted = sorted(ranked, key=functools.cmp_to_key(Puzzle.cmp_ranked))
    position = 1
    total = 0
    for ra in rsorted:
      winnings = position * ra[2]
      print(ra, position, winnings)
      position = position + 1
      total = total + winnings
    print('Total Winnings', total)



if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

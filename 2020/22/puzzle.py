class Puzzle:

  def process(self, text):
    self.player = [[],[]]
    curplayer = 0
    lines = text.split('\n')

    for line in lines:
      if line == 'Player 1:':
        pass
      elif line == 'Player 2:':
        curplayer = 1
      elif line.strip() != '':
        num = int(line)
        self.player[curplayer].append(num)

  def play_round(self):
    p1 = self.player[0].pop(0)
    p2 = self.player[1].pop(0)
    if p1 > p2:
      self.player[0].append(p1)
      self.player[0].append(p2)
      return 0
    else:
      self.player[1].append(p2)
      self.player[1].append(p1)
      return 1

  def _recursive_play(self, p1deck, p2deck, indent=''):
    seen = []
    round = 0
    while len(p1deck) > 0 and len(p2deck) > 0:
      board = (p1deck, p2deck)
      if board in seen:
        return (0, p1deck, p2deck) #Recursion, p1 wins
      else:
        round += 1
        print indent, 'Round:', round
        print indent, p1deck
        print indent, p2deck
        seen.append(board)
        p1 = p1deck[0]
        p2 = p2deck[0]
        if p1+1 <= len(p1deck) and p2+1 <= len(p2deck):
          #print 'Recurse Again', p1, p2
          winner, _, _ = self._recursive_play(p1deck[1:p1+1], p2deck[1:p2+1], indent + '> ')
        else:
          if p1 > p2:
            winner = 0
          else:
            winner = 1
        #print indent + 'winner', winner+1
        if winner == 0:
          p1deck = p1deck[1:] + [p1, p2]
          p2deck = p2deck[1:]
        else:
          p1deck = p1deck[1:]
          p2deck = p2deck[1:] + [p2, p1]
    if len(p1deck) > 0:
      return (0, p1deck, p2deck)
    else:
      return (1, p1deck, p2deck)

  def play_recursive_combat(self, p1deck, p2deck):
    return self._recursive_play(p1deck, p2deck)

  def score_deck(self, deck):
    count = len(deck)
    score = 0
    for i in range(count):
      score += (deck[i] * (count-i))
    return score


  def result1(self):
    round = 1
    while len(self.player[0]) != 0 and len(self.player[1]) != 0:
      winner = self.play_round()
      print 'Round', round, 'winner', winner + 1
    print 'Finished'
    print 'Player 1:', self.player[0]
    print 'Player 2:', self.player[1]
    if len(self.player[0]) > 0:
      windeck = self.player[0]
    else:
      windeck = self.player[1]
    print 'Winning Score', self.score_deck(windeck)

  def result(self):
    winner, p1deck, p2deck = self.play_recursive_combat(self.player[0], self.player[1])
    print 'Win:', winner
    print p1deck, self.score_deck(p1deck)
    print p2deck, self.score_deck(p2deck)


if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

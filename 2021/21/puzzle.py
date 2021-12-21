class Puzzle:
  def calc_space(self, start, player, roll):
    bases = {1: 0, 2: 3}
    base = bases[player]
    n = (((roll-1) * 6)+1+base)
    dice = ((n-1) % 100) + 1 + ((n) % 100) + 1 + ((n+1) % 100) + 1
    #print 'P', player, 'N:', n, 'D:', dice
    #dice = dice % 100
    space = start + dice
    space = (space - 1) % 10
    space = space + 1
    return space

  def simulate(self, start, player, rolls = None):
    print 'Player:'
    space = start
    score = 0
    roll = 0
    if rolls:
      for roll in range(rolls):
        space = self.calc_space(space, player, roll+1)
        score += space
    else:
      while score < 1000:
        #print space
        space = self.calc_space(space, player, roll+1)
        score += space
        roll += 1
    return score, roll
    
  def result(self):
    #Player 1 starting position: 10
    #Player 2 starting position: 6
    players = [10, 6]
    winner = 1
    loser = 2

    score, roll = self.simulate(players[winner-1], winner)
    print 'Score', score, 'Player rolled', (roll*3), 'times'
    total_rolls = roll * 3
    if winner == 1:
      rolls = roll - 1
    else:
      rolls = roll - 2
    score, roll = self.simulate(players[loser-1], loser, rolls)
    print 'Score', score, 'Player rolled', (roll*3), 'times'
    total_rolls += (roll * 3) + 3
    print 'Loser Calc', score * total_rolls
    

if __name__ == '__main__':
  puz = Puzzle()
  puz.result()

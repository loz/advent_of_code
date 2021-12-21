#Scores : number of universes with this roll move
moves = { 3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1 }
#moves = {5: 6, 6: 7, 7: 6}

known_results = {
}

class Puzzle:
  def calc_space(self, start, player, roll):
    bases = {1: 0, 2: 3}
    base = bases[player]
    n = (((roll-1) * 6)+1+base)
    dice = ((n-1) % 100) + 1 + ((n) % 100) + 1 + ((n+1) % 100) + 1
    space = start + dice
    space = (space - 1) % 10
    space = space + 1
    return space

  def simulate_fixed_dice(self, players, diceroll):
    player = 0
    scores = [0,0]
    inc = diceroll * 3
    win = False
    #for roll in range(100):
    roll = 0
    universes = 1
    while not win:
      newpos = (players[player] + inc - 1) % 10
      scores[player] += newpos
      roll += 3
      universes *= 27
      if scores[player] >= 21:
        win = True
      players[player] = newpos
      player = 1 - player
      print roll, players, 'Scores', scores
    print 3**roll, 'Universes', universes

  def simulate_universes(self, players, scores, curplayer):
    key = (players[0], players[1], scores[0], scores[1], curplayer)
    if key in known_results:
      #print 'Cache hit!'
      return known_results[key]
    wins = [0, 0]
    for move in moves:
      score = ((players[curplayer] + move - 1) % 10) + 1
      newscore = scores[curplayer] + score
      if newscore >= 21:
        #They win in N univeses with this win in
        #print 'Win', curplayer, newscore, scores, moves[move]
        #print 'Wins with move', move, 'in', moves[move], 'universes'
        wins[curplayer] += moves[move] 
        #wins[curplayer] += 1
      else:
        newplayers = [players[0], players[1]]
        newscores = [scores[0], scores[1]]
        newplayers[curplayer] = score
        newscores[curplayer] = newscore
        rwins = self.simulate_universes(newplayers, newscores, 1 - curplayer )
        #This occurs in N universes with these results
        wins[0] += (moves[move] * rwins[0])
        wins[1] += (moves[move] * rwins[1])
        #wins[0] += rwins[0]
        #wins[1] += rwins[1]
    known_results[key] = wins
    return wins

  def result(self):
    #Worst case leads to around: 5559060566555520 universes

    players = [10, 6]
    #players = [4, 8]

    wins = self.simulate_universes(players, [0, 0], 0)
    print wins
    #print known_results
    #All universes roll 1
    #self.simulate_fixed_dice(players, 1)
    #All universes roll 2
    #self.simulate_fixed_dice(players, 2)
    #All universes roll 3
    #self.simulate_fixed_dice(players, 3)
    

if __name__ == '__main__':
  puz = Puzzle()
  puz.result()

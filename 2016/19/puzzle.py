class Puzzle:

  def process(self, size):
    self.game = {}
    self.chain = {}
    for i in range(size):
      self.game[i+1] = 1
      self.chain[i+1] = ((i+1) % size) + 1

  def play_game(self):
    player = self.chain.keys()[0]
    remaining = len(self.chain.keys())
    while remaining > 1:
      nextplayer = self.chain[player]
      skipplayer = self.chain[nextplayer]
      self.game[player] += self.game[nextplayer] #takes their present
      self.game[nextplayer] = 0
      self.chain[player] = skipplayer
      self.chain.pop(nextplayer)
      remaining -= 1
      player = skipplayer
      #print player, remaining
    return self.chain.keys()[0]

  def find_opposite(self,  player, remaining):
    half = remaining / 2
    #print half
    opposite = player
    prev = None
    for i in range(half):
      prev = opposite
      opposite = self.chain[opposite]
    #print opposite, prev
    return opposite, prev

  def play_game2(self):
    player = self.chain.keys()[0]
    remaining = len(self.chain.keys())
    op_player, prev = self.find_opposite(player, remaining)

    while remaining > 1:
      #op_player, prev = self.find_opposite(player, remaining)
      print player, 'steals', op_player
      skipplayer = self.chain[op_player]

      self.game[player] += self.game[op_player] #takes their present
      self.game[op_player] = 0
      self.chain[prev] = skipplayer
      self.chain.pop(op_player)
      remaining -= 1
      player = self.chain[player]
      if remaining % 2 == 0:
        prev = skipplayer
        op_player = self.chain[prev]
      else:
        op_player = skipplayer
      #print player, remaining
    return self.chain.keys()[0]

  def result(self):
    count = 3014603
    print 'Playing with', count, 'elves'
    self.process(count)
    print 'Winner:', self.play_game2()

if __name__ == '__main__':
  puz = Puzzle()
  puz.result()

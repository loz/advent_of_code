import numpy as np

class Puzzle:

  def process(self, text):
    self.calls = []
    self.boards = []
    lines = text.split('\n')
    lines = self.process_calls(lines)
    self.process_boards(lines)

  def process_calls(self, lines):
    first = lines[0]
    self.calls = map(lambda x: int(x), first.split(','))
    rest = lines [2:]
    return rest

  def process_boards(self,lines):
    board = []
    for line in lines:
      if len(line) != 0:
        row = map(lambda x: int(x), line.split())
        board.append(row)
      else:
        self.boards.append(board)
        board = []

  def play_bingo(self):
    self.winning_board = None
    self.last_call = None
    for number in self.calls:
      self.last_call = number
      self.dab(number)
      if self.is_winner():
        self.winning_score = self.score_board(self.winning_board) * number
        return

  def score_board(self, boardid):
    board = self.boards[boardid]
    score = 0
    for row in board:
      for num in row:
        if num != '*':
          score += num
    return score

  def is_winner(self):
    for idx, board in enumerate(self.boards):
      for row in board:
        if row == ['*', '*', '*', '*', '*']:
          self.winning_board = idx
          return True
      #transpose rows to columns
      tboard = np.array(board).T.tolist()
      for row in tboard:
        if row == ['*', '*', '*', '*', '*']:
          self.winning_board = idx
          return True


  def dab(self, number):
    for board in self.boards:
      for row in board:
        hit = row.index(number) if number in row else None
        if hit != None:
          row[hit] = '*'

  def result(self):
    self.play_bingo()
    print self.winning_score

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

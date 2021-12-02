class Puzzle:

  def __init__(self):
    self.horizontal = 0
    self.depth = 0
    self.aim = 0

  def process(self, text):
    commands = text.split('\n')
    for command in commands:
      if len(command) == 0:
        return
      self.process_command(command)

  def process_command(self, command):
    op, val = command.split()
    val = int(val)
    if op == 'forward':
      self.horizontal += val
      self.depth += val * self.aim
    elif op == 'up':
      self.aim -= val
    else: #down
      self.aim += val


  def result(self):
    print 'Horiz', self.horizontal
    print 'Depth', self.depth
    print 'Result', self.horizontal * self.depth

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()

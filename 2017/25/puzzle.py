import sys
class Node:
  def __init__(self):
    self.value = 0
    self.left = None
    self.right = None

  def leftmost(self):
    return self.left == None

  def rightmost(self):
    return self.right == None

  def goleft(self):
    if self.left == None:
      newnode = Node()
      newnode.right = self
      self.left = newnode
    return self.left

  def goright(self):
    if self.right == None:
      newnode = Node()
      newnode.left = self
      self.right = newnode
    return self.right

class Puzzle:
  def __init__(self):
    self.head = Node()

  def left(self):
    newhead = self.head.goleft()
    self.head = newhead

  def right(self):
    newhead =  self.head.goright()
    self.head = newhead

  def read(self):
    return self.head.value

  def write(self, value):
    self.head.value = value

  def checksum(self):
    head = self.head
    #print 'H:', head, head.left, head.right
    while not head.leftmost():
      #print 'L:', head, head.left, head.right
      head = head.goleft()
    total = head.value
    while not head.rightmost():
      head = head.goright()
      #print 'R:', head, head.value, head.left, head.right
      total += head.value
    return total

  def dump(self):
    head = self.head
    while not head.leftmost():
      head = head.goleft()
    while not head.rightmost():
      if head == self.head:
        sys.stdout.write('[' + str(head.value) + ']')
      else:
        sys.stdout.write(str(head.value))
      head = head.goright()
    if head == self.head:
      sys.stdout.write('[' + str(head.value) + ']')
    else:
      sys.stdout.write(str(head.value))

    print ' about to run state', self.currentstate
    

  def process(self, text):
    self.states = {}
    for chunk in text.split('In state '):
      self.process_chunk(chunk)

  def process_chunk(self, chunk):
    if chunk != '':
      if chunk.startswith('Begin'):
        self.process_initial_state(chunk)
      else:
        self.process_node(chunk)

  def process_initial_state(self, chunk):
    lines = chunk.split('\n')
    begin = lines[0]
    perf = lines[1]
    begin = begin.replace('Begin in state ', '')
    begin = begin.replace('.', '')
    self.start = begin
    perf = perf.replace('Perform a diagnostic checksum after ', '')
    perf = perf.replace(' steps.', '')
    self.steps = int(perf)

  def process_node(self, chunk):
    lines = chunk.split('\n')
    label = lines.pop(0)
    label = label.replace(':', '')
    conditions = []
    val = None
    move = None
    newstate = None
    for line in lines:
      if line.startswith('  If'):
        pass
      elif line.startswith('    - Write'):
        val = line.replace('    - Write the value ', '')
        val = val.replace('.', '')
        val = int(val)
      elif line.startswith('    - Move'):
        move = line.replace('    - Move one slot to the ', '')
        move = move.replace('.', '')
      elif line.startswith('    - Continue'):
        newstate = line.replace('    - Continue with state ', '')
        newstate = newstate.replace('.', '')
        conditions.append((val, move, newstate))
    
    self.states[label] = conditions

  def step(self):
    val = self.read()
    action = self.states[self.currentstate][val]
    val, move, newstate = action
    self.write(val)
    if move == 'left':
      self.left()
    else:
      self.right()
    self.currentstate = newstate

  def result(self):
    self.currentstate = self.start
    #self.dump()
    for i in range(self.steps):
      self.step()
      #self.dump()
    print 'Checksum:', self.checksum()


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

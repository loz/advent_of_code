import sys
from colorama import Fore

class Machine:
  def __init__(self):
    self.reset()

  def reset(self):
    self.ip = 0
    self.a = 0
    self.b = 0
    self.c = 0
    self.output = []
 
  def execute_all(self):
    while self.execute():
      pass

  def execute_match(self):
    while self.execute():
      if self.program[:len(self.output)] != self.output:
        return False

  def fetch(self):
    i = self.program[self.ip]
    if self.ip == len(self.program)-1:
      return (i, None, None)
    o = self.program[self.ip+1]
    combo = o
    if o == 4:
      combo = self.a
    elif o == 5:
      combo = self.b
    elif o == 6:
      combo = self.c
    elif o == 7:
      combo = None

    return (i, o, combo)

  def transpile(self):
    ip = 0
    while ip < len(self.program):
      inst, operand = self.program[ip], self.program[ip+1]
      ip += 2

      if operand == 4:
        combo = 'a'
      elif operand == 5:
        combo = 'b'
      elif operand == 6:
        combo = 'c'
      else:
        combo = str(operand)

      if inst == 0: #adv
        print('adv: a = a // (2**' + combo + ')')
      elif inst == 1: #bxl
        print('bxl: b = b ^ ' + str(operand))
      elif inst == 2: #bst
        print('bst: b = ' + combo + ' % 8')
      elif inst == 3: #jnz
        print('jze:', operand)
      elif inst == 4: #bxc
        print('bxl: b = b ^ c')
      elif inst == 5: #out
        print('out: ' + combo + ' % 8')
      elif inst == 6: #bdv
        print('bdv: b = a // (2**' + combo + ')')
      elif inst == 7: #cdv
        print('cdv: c = a // (2**' + combo + ')')
      else:
        raise 'Not Implemented'

    
    
  def execute(self):
    if self.ip >= len(self.program):
      return False

    inst, operand, combo = self.fetch()
    #print('i', inst, 'o', operand, 'c', combo)
    if inst == 0: #adv
      self.a = int(self.a / (2**combo))
    elif inst == 1: #bxl
      self.b = self.b ^ operand
    elif inst == 2: #bst
      self.b = combo % 8
    elif inst == 3: #jnz
      if self.a != 0:
        self.ip = operand - 2
    elif inst == 4: #bxc
      self.b = self.b ^ self.c
    elif inst == 5: #out
      self.output.append( combo % 8 )
    elif inst == 6: #bdv
      #self.b = self.a // (2**combo)
      self.b = int(self.a / (2**combo))
    elif inst == 7: #cdv
      #self.c = self.a // (2**combo)
      self.c = int(self.a / (2**combo))
    else:
      raise 'Not Implemented'

    self.ip += 2
    return True

class Puzzle:

  def process(self, text):
    self.machine = Machine()

    state, code = text.split('\n\n')
    for line in state.split('\n'):
      self.process_state(line)
    
    self.process_code(code)

  def process_code(self, code):
    _, code = code.split(': ')
    self.machine.program = [int(v) for v in code.split(',')]

  def process_state(self, line):
      left, right = line.split(': ')
      _, left = left.split(' ')
      val = int(right)
      if left == 'A':
        self.machine.a = val
      elif left == 'B':
        self.machine.b = val
      else:
        self.machine.c = val

  def result(self):
    print('Initializing New Machine')
    a = 0
    self.machine.transpile()
    return
    searching = True
    while searching:
      self.machine.reset()
      self.machine.a = a
      #machine.execute_all()
      self.machine.execute_match()
      if self.machine.output == self.machine.program:
        print('Found! A=', a)
        return
      else:
        if a % 10000 == 0:
          print('.', end='', flush=True)
        a = a + 1


  def result1(self):
    print(self.machine.a)
    print(self.machine.b)
    print(self.machine.c)
    print(self.machine.program)
    while self.machine.execute():
      pass
    print('Output:', self.machine.output)
    print(','.join([str(x) for x in self.machine.output]))


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

import sys

class Module:
  def __init__(self, name):
    self.name = name
    self.inputs = []
    self.outputs = []

  def gname(self):
    tmap = {
      'button': 'btn',
      'flip-flop':'ff',
      'conjunction':'c',
      'output': 'o'
    }
    return self.name + '_' + tmap[self.type]

  def requires(self, source, signal):
    needs = []
    for i in self.inputs:
      needs.append((i, signal))
    return needs

  def output(self, signal):
    for o in self.outputs:
      self.board.signals.append((signal, self.name, o))

  def send_signal(self, pulse):
    smap = {0:'-low', 1:'-high'}
    signal, pfrom, pto = pulse
    if pto == self.board.target and signal == 1:
      if pfrom not in self.board.cycles:
        print('High To Target', self.board.target, 'on', self.board.presses, 'from', pfrom)
        self.board.cycles[pfrom] = self. board.presses

    self.board.pulses[signal] += 1
    #print(pfrom, smap[signal] + '->', pto)
    mod = self.board.lookup(pto)
    mod.pulse(signal, pfrom)

class Button(Module):
  def __init__(self, name):
    super().__init__(name)
    self.type = 'button'

  def pulse(self):
    self.output(0)
    self.board.pulses[0] += 1 #button signal
    while(self.board.signals):
      signal = self.board.signals.pop(0)
      self.send_signal(signal)

class FlipFlip(Module):
  def __init__(self, name):
    super().__init__(name)
    self.type = 'flip-flop'
    self.state = 0

  def pulse(self, signal, source):
    if signal == 0:
      self.state = 1 - self.state
      self.output(self.state)

  def requires(self, source, signal):
    needs = []
    #for i in self.inputs:
    #  needs.append((i, 'F'+str(signal)))
    return needs

class Conjunction(Module):
  def __init__(self, name):
    super().__init__(name)
    self.type = 'conjunction'
    self.memory = None

  def init_mem(self):
    self.memory = {}
    for i in self.inputs:
      self.memory[i] = 0

  def requires(self, source, signal):
    needs = []
    if signal == 0:
      for i in self.inputs:
        needs.append((i, 1))
    else:
      for i in self.inputs:
        needs.append((i, 0))

    return needs

  def pulse(self, signal, source):
    if(self.memory == None):
      self.init_mem()
    self.memory[source] = signal
    all1 = True
    for v in self.memory.values():
      if v != 1:
        all1 = False

    if all1:
      self.output(0)
    else:
      self.output(1)

class Output(Module):
  def __init__(self, name):
    super().__init__(name)
    self.type = 'output'
    self.low_count = 0
    self.high_count = 0
    self.last = 0

  def pulse(self, signal, source):
    self.last = signal
    if signal == 1:
      self.high_count += 1
    else:
      self.low_count += 1

class Puzzle:

  def process(self, text):
    self.modules = {}
    self.signals = []
    self.pulses = {0:0, 1:0}
    mod = Output('output')
    mod.board = self
    self.modules['output'] = mod
    self.output = mod
    for line in text.split('\n'):
      self.process_line(line)
    self.connect_inputs()
    self.outputs = []
    for m in self.modules:
      mod = self.modules[m]
      if mod.type == 'flip-flop':
        self.outputs.append(m)
    self.outputs = sorted(self.outputs)

  def connect_inputs(self):
    names = list(self.modules.keys())
    for m in names:
      mod = self.modules[m]
      for o in mod.outputs:
        target = self.lookup(o)
        target.inputs.append(mod.name)

  def lookup(self, name):
    mod = self.modules.get(name, None)
    if mod == None: #an output
      mod = Output(name)
      self.modules[name] = mod
    return mod

  def process_line(self, line):
    if line != '':
      name, mappings = line.split(' -> ')
      outs = mappings.split(', ')
      if name[0] == '%':
        name = name[1:]
        mod = FlipFlip(name)
        mod.outputs = outs
        mod.board = self
        self.modules[name] = mod
      elif name[0] == '&':
        name = name[1:]
        mod = Conjunction(name)
        mod.outputs = outs
        mod.board = self
        self.modules[name] = mod
      else:
        mod = Button('broadcaster')
        mod.outputs = outs
        mod.board = self
        self.modules['broadcaster'] = mod
        self.broadcaster = mod

  def dumpouts(self):
    for m in self.outputs:
      mod = self.modules[m]
      #sys.stdout.write(mod.name +  ':' + str(mod.state) + ' ')
      sys.stdout.write(str(mod.state))
    sys.stdout.write('\n')

  def result(self):
    self.result2()

  def walkback(self, name, need, seen = []):
    mod = self.modules[name]
    needs = mod.requires(name, need)
    print(name, ':', need, '<-', needs)
    for nm, sig in needs:
      #if nm not in seen:
      #  self.walkback(nm, sig, seen + [name])
      self.walkback(nm, sig, seen + [name])


  def dumpheads(self, outs):
    for bits in outs:
      for o in bits:
        sys.stdout.write(o[0])
      sys.stdout.write(' | ')
    sys.stdout.write('\n')
    for bits in outs:
      for o in bits:
        sys.stdout.write(o[1])
      sys.stdout.write(' | ')
    sys.stdout.write('\n')
    for bits in outs:
      for o in bits:
        sys.stdout.write('-')
      sys.stdout.write('-+-')
    sys.stdout.write('\n')


  def dumpouts(self, outs):
    for bits in outs:
      for m in bits:
        mod = self.modules[m]
        sys.stdout.write(str(mod.state))
      sys.stdout.write(' | ')
    sys.stdout.write('\n')
  
  def spitgraph(self):
    print('===== GRAPH =====')
    for m in self.modules:
      mod = self.modules[m]
      for o in mod.outputs:
        d = self.modules[o]
        print(mod.gname(), '->', d.gname(), ';')
    print('=================')
    pass

  def result2(self):
    term = self.lookup('rx')
    (bits,) = term.inputs
    fed = self.lookup(bits)
    print('End Node', 'input', term.inputs)
    print('Fed by', fed.inputs)
    self.cycles = {}
    self.target = bits
    print('Searching for Cycles')

    self.presses = 0
    done = False
    sources = fed.inputs
    while(not done):
      done = True
      self.presses += 1
      self.broadcaster.pulse()
      for f in sources:
        if f not in self.cycles:
          done = False
    print(self.cycles)
    total = 1
    for v in self.cycles.values():
      total *= v
    print('Answer is LCM of these numbers:', total)

  def result2_old(self):
    #self.spitgraph()
    #return
    bits = [
      #['vd', 'ld', 'bn', 'fq', 'rs', 'zz', 'sq', 'mb'],
      ['fq', 'ld', 'mb', 'vd', 'bn', 'sq', 'rs', 'zz'],
      ['mx', 'zd'],

      ['jh', 'st',           'rc', 'rk', 'xt', 'jj', 'mf', 'bv', 'fn'],
      ['bt', 'zp'],

      ['rl', 'fx',           'dx', 'fz', 'km', 'xp', 'mv', 'ch', 'tp'],

      ['lq', 'rf', 'dg', 'qm', 'kc', 'js', 'lp'],
      ['gz', 'lg', 'xf', 'qr', 'tq', 'xh', 'lr', 'ct', 'sv', 'fj', 'gv']
    ]
    seen = []
    print ('='*40 + "START" + '='*40)
    for bit in bits:
      for b in bit:
        seen.append(b)
    rest = []
    for o in self.outputs:
      if o not in seen:
        rest.append(o)

    bits.append(rest)

    self.dumpheads(bits)
    #Skim already scanned
    #for i in range(10*100):
    #  self.broadcaster.pulse()

    for i in range(10):
      print('===== 100 =======')
      for i in range(100):
        self.broadcaster.pulse()
        self.dumpouts(bits)
    #self.walkback('rx', 0)

  def result2_brute(self):
    presscount = 0
    rx = self.lookup('rx')
    print(rx)
    while(True):
      for i in range(10000):
        presscount += 1
        self.broadcaster.pulse()
        if rx.low_count > 0:
          print('Hit RX!', presscount)
          return
      sys.stdout.write('.')
      sys.stdout.flush()

  def result1(self):
    print('Pulsing 1000')
    for i in range(1000):
    #for i in range(4):
      #print('====== PRESS ==========')
      self.broadcaster.pulse()
    print('High', self.pulses[1])
    print('Low', self.pulses[0])
    print('Total', self.pulses[0] * self.pulses[1])


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

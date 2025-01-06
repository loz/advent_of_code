import sys
from colorama import Fore
from math import factorial
from itertools import combinations

def n_choose_m(n, m):
  if n >= m:
    combo = int(factorial(n) / (factorial(n-m) * factorial(m)))
  else:
    combo = n
  return combo

class Wire:
  def __init__(self, name):
    self.state = None
    self.name = name
    self.outputs = []

  def __str__(self):
    outs = ','.join([g.name for g in self.outputs])
    return 'W(' + self.name + ': ' + outs + ')'

  def connect(self, item):
    self.outputs.append(item)

  def send(self, value):
    self.state = value
    for o in self.outputs:
      o.send(value)

class Gate:
  def __init__(self, name):
    self.name = name
    self.outputs  = {}
    self.reset()

  def __str__(self):
    return 'G(' + self.name + ')'

  def reset(self):
    self.recieved = []

  #Connect to each output
  def connect(self, gate):
    self.outputs[gate.name] = gate

  def send(self, value):
    self.recieved.append(value)

  def sendon(self, value):
    for k in self.outputs:
      gate = self.outputs[k]
      gate.send(value)

class AndGate(Gate):
  def label(self):
    return ("AND", "square")

  def send(self, value):
    super().send(value)
    if len(self.recieved) == 2:
      a, b = self.recieved
      if a == 1 and b == 1:
        self.sendon(1)
      else:
        self.sendon(0)

class OrGate(Gate):
  def label(self):
    return ("OR", "diamond")

  def send(self, value):
    super().send(value)
    if len(self.recieved) == 2:
      a, b = self.recieved
      if a == 1 or b == 1:
        self.sendon(1)
      else:
        self.sendon(0)

class XorGate(Gate):
  def label(self):
    return ("XOR", "circle")

  def send(self, value):
    super().send(value)
    if len(self.recieved) == 2:
      a, b = self.recieved
      if a != b:
        self.sendon(1)
      else:
        self.sendon(0)

class Puzzle:
  def __init__(self):
    self.initial = {}
    self.wires = {}

  def process(self, text):
    initial, wiring = text.split('\n\n')

    for line in initial.split('\n'):
      self.process_starts(line)

    self.numgates = 0
    self.allgates = []
    for line in wiring.split('\n'):
      self.process_wiring(line)

  def process_starts(self, line):
    if line != '':
      name, val = line.split(': ')
      self.initial[name] = int(val)

  def find_or_create(self, name):
    if name not in self.wires:
      self.wires[name] = Wire(name)
    return self.wires[name]

  def process_wiring(self, line):
    if line != '':
      self.numgates += 1
      a, gatetype, b, _, dest = line.split(' ')

      wirea = self.find_or_create(a)
      wireb = self.find_or_create(b)
      dest = self.find_or_create(dest)
      
      gate = None
      if gatetype == 'AND':
        gate = AndGate(line)
      elif gatetype == 'OR':
        gate = OrGate(line)
      else:
        gate = XorGate(line)
      gate.idx = self.numgates
      self.allgates.append(gate)

      wirea.connect(gate)
      wireb.connect(gate)
      gate.connect(dest)

  def wire(self, name):
    return self.wires[name]

  def trigger_initial(self):
    for key in self.initial:
      wire = self.wires[key]
      wire.send(self.initial[key])

  def fetch_value(self, letter):
    names = self.wires.keys()
    names = sorted(names, reverse=True)
    value = ''
    for name in names:
      if name.startswith(letter):
        value += str(self.wires[name].state)
    return value

  def diff(self, a, b):
    diff = ''
    if len(b) < len(a):
      extra = len(a)-len(b)
      left = a[:extra]
      a = a[extra:]
      diff = Fore.CYAN + left + Fore.RESET
    elif len(a) < len(b):
      extra = len(b)-len(a)
      left = b[:extra]
      b = b[extra:]
      #diff = Fore.CYAN + left + Fore.RESET

    for i, ch in enumerate(a):
      if i < len(b) and ch != b[i]:
        diff += Fore.RED + ch + Fore.RESET
      else:
        diff += ch
    return diff

  def diffbits(self, a, b):
    if len(b) < len(a):
      extra = len(a)-len(b)
      left = a[:extra]
      a = a[extra:]
      diff = Fore.CYAN + left + Fore.RESET

    nn = len(a)
    bits = []
    for i, ch in enumerate(a):
      if ch != b[i]:
        num = nn-i-1
        bits.append("z{0:0>2d}".format(num))
    return bits

  def find_inputs(self, bits):
    inputs = set()
    targets = set()
    for name in self.wires:
      wire = self.wires[name]
      gates = wire.outputs
      for g in gates:
        tolist = list(g.outputs.keys())
        if set(tolist) - set(bits) != set(tolist):
          targets.add(g)
          inputs.add(wire.name)
    return (inputs, targets)

  def result(self):
    self.result2()

  def execute(self):
    self.trigger_initial()
    xvalue = self.fetch_value('x')
    yvalue = self.fetch_value('y')
    zvalue = self.fetch_value('z')
    x = int(xvalue, 2)
    y = int(yvalue, 2)
    z = int(zvalue, 2)
    t = x + y
    tvalue = '{0:0b}'.format(t)
    padding = max(len(xvalue), len(yvalue), len(zvalue), len(tvalue))
    print('X:', ' '*(padding-len(xvalue)), xvalue, x)
    print('Y:', ' '*(padding-len(yvalue)), yvalue, y)
    print('T:', ' '*(padding-len(tvalue)), tvalue, t)
    print('Z:', ' '*(padding-len(zvalue)), self.diff(zvalue, tvalue), z)


  def result2(self):
    self.execute()
    #self.dump_graph()
    """
    Plan:
    Viewing the above graph, we can see the construction of
    the circuit.

    The circuit is supposed to ADD two numbers, using
    chains of ADDER blocks.

    Generate the correct ADDER circuit
    diff correct vs incorrect
    -> the wires which need to be changed

    Challenge: we will need to ALIAS intermediary
      steps as our carry/result will have differnent names

    ADDER   [Bit 0]

      bitx, bity
      x XOR y -> z  *
      x AND y -> carry *

    ADDER with CARRY  [Bits 1+]

      bitx, bity, carry

      x XOR y -> i1
      i1 XOR c -> z  *
      x AND y -> i2
      i1 AND c -> i3
      i2 OR i3 -> c  *
    """
    tmpcount = 0
    xvalue = self.fetch_value('x')
    numbits = len(xvalue)
    wires = []
    carry = None
    for bit in range(numbits):
      carry, circuit, tmpcount = self.gen_adder(bit, carry, tmpcount)
      wires.extend(circuit)
      #print(carry, circuit)

    goodwires = {}
    for wire in wires:
      goodwires[wire.name] = wire
    """
    #replace to test
    self.wires = {}
    allgates = set()
    for wire in wires:
      self.wires[wire.name] = wire
      for g in wire.outputs:
        allgates.add(g)

    self.allgates = []
    for i, gate in enumerate(allgates):
      gate.idx = i
      self.allgates.append(gate)
  
    print('My Circuit')
    self.execute()
    return
    """

    #TODO: Compare self.wires with wires
    print('Diffing correct vs given wires')
    goodgates = set()
    for name in goodwires:
      wire = goodwires[name]
      for g in wire.outputs:
        goodgates.add(g)

    # Relable wires in GOOD circuit with BAD to find issues
    goodkeys = set(goodwires.keys())
    badkeys = set(self.wires.keys())

    #print(goodkeys)
    #print(badkeys)
    tovisit = list(goodkeys & badkeys)
    mapped = {}
    visited = {}

    for name in tovisit:
      mapped[name] = name #We don't remap starter/ends

    errors = set()

    while(tovisit):
      name = tovisit.pop()
      if name in visited:
        next
      visited[name] = True
      good = goodwires[name]
      bad  = self.wires[name]
      if len(good.outputs) != len(bad.outputs):
        #print(name, 'does not match good circuit')
        #print('good', [g.name for g in good.outputs])
        #print('bad ', [g.name for g in bad.outputs])
        errors.add(name)

      good_xor = self.find_xor(good.outputs)
      bad_xor  = self.find_xor(bad.outputs)
      errors |= self.map_wires(good_xor, bad_xor, 'XOR', mapped, tovisit, goodwires, goodgates)

      good_or  = self.find_or(good.outputs)
      bad_or   = self.find_or(bad.outputs)
      errors |= self.map_wires(good_or, bad_or, 'OR', mapped, tovisit, goodwires, goodgates)

      good_and = self.find_and(good.outputs)
      bad_and  = self.find_and(bad.outputs)
      errors |= self.map_wires(good_and, bad_and, 'AND', mapped, tovisit, goodwires, goodgates)

    print(errors)
    errors = sorted(errors)
    print('Answer:', ','.join(errors))

  def rename_wire(self, wire, newname, goodgates, goodwires):
    oldname = wire.name
    for g in goodgates:
      if oldname in g.outputs:
        g.outputs.pop(oldname)
        g.outputs[newname] = wire
    goodwires.pop(oldname)
    goodwires[newname] = wire
    wire.name = newname

  def map_wires(self, goodgate, badgate, gatetype, mapped, tovisit, goodwires, goodgates):
    errors = set()
    if goodgate:
      if not badgate:
        #print('Bad Missing:>> '+ gatetype, goodgate.name)
        pass
      else:
        goodname = list(goodgate.outputs.keys())[0]
        badname  = list(badgate.outputs.keys())[0]
        if goodname != badname: #Remap
          if goodname in mapped and mapped[goodname] != badname:
            #print('Collision', mapped[goodname], 'v', badname)
            errors.add(goodname)
            errors.add(badname)
          else:
            good = goodwires[goodname]
            bad = self.wires[badname]
            #print('Mapping', goodname, badname, good, bad)
            self.rename_wire(good, badname, goodgates, goodwires)
            mapped[goodname] = badname
            tovisit.append(badname)
    elif badgate:
      #print('Badgate Extra? ' + gatetype, badgate.name)
      pass
    return errors
  
  def find_other_input(self, gate, thisone):
    for name in self.wires:
      wire = self.wires[name]
      if wire != thisone:
        if gate in wire.outputs:
          return wire.name, wire
    return None

  def find_xor(self, gates):
    for g in gates:
      tt, _ = g.label()
      if tt == 'XOR':
        return g

  def find_or(self, gates):
    for g in gates:
      tt, _ = g.label()
      if tt == 'OR':
        return g

  def find_and(self, gates):
    for g in gates:
      tt, _ = g.label()
      if tt == 'AND':
        return g

  def gen_adder(self, bit, carry, tmpcount):
    wires = []
    x = "x{:0>2}".format(bit)
    y = "y{:0>2}".format(bit)
    z = "z{:0>2}".format(bit)
    c = "c{:0>2}".format(bit)
    wx = Wire(x)
    wy = Wire(y)
    wz = Wire(z)
    wc = Wire(c)
    wires.extend([wx, wy, wz, wc])

    if not carry:
      #print('ADDER')
      """
      bitx, bity
      x XOR y -> z  *
      x AND y -> carry *
      """
      gate = XorGate('x XOR y -> z')
      wx.connect(gate)
      wy.connect(gate)
      gate.connect(wz)
      
      gate = AndGate('x AND y -> c')
      wx.connect(gate)
      wy.connect(gate)
      gate.connect(wc)
    else:
      #print('ADDER with CARRY')
      """
      x XOR y -> i1
      i1 XOR c -> z  *
      x AND y -> i2
      i1 AND c -> i3
      i2 OR i3 -> c  *
      """
      gate = XorGate('x XOR y -> i1')
      i1 = "i{:0>2}".format(tmpcount)
      tmpcount += 1
      wi1 = Wire(i1)
      wx.connect(gate)
      wy.connect(gate)
      gate.connect(wi1)

      gate = XorGate('i1 XOR carry -> z')
      wi1.connect(gate)
      carry.connect(gate)
      gate.connect(wz)

      gate = AndGate('x and y -> i2')
      i2 = "i{:0>2}".format(tmpcount)
      tmpcount += 1
      wi2 = Wire(i2)
      wx.connect(gate)
      wy.connect(gate)
      gate.connect(wi2)

      gate = AndGate('i1 AND c -> i3')
      i3 = "i{:0>2}".format(tmpcount)
      tmpcount += 1
      wi3 = Wire(i3)
      wi1.connect(gate)
      carry.connect(gate)
      gate.connect(wi3)

      gate = OrGate('i2 OR i3 -> c')
      wi2.connect(gate)
      wi3.connect(gate)
      gate.connect(wc)
      wires.extend([wi1, wi2, wi3])
      
    return wc, wires, tmpcount


  def dump_graph(self):
    print("Here's a Graph:")
    print("digraph G {")
    for gate in self.allgates:
      label, shape = gate.label()
      print("   GATE" + str(gate.idx) + '[label="' + label + '" shape="' + shape + '"];') 
    print('')

    for name in self.wires:
      wire = self.wires[name]
      for o in wire.outputs:
        oname = "GATE" + str(o.idx)
        print("   " + name  + " -> " + oname)
    print('')

    for gate in self.allgates:
      oname = "GATE" + str(gate.idx)
      for o in gate.outputs:
        print("   " + oname + " -> " + o)

    print("}")

  def result1(self):
    self.trigger_initial()
    names = self.wires.keys()
    names = sorted(names)
    for name in names:
      print(name, self.wires[name].state)
    zvalue = self.fetch_value('z')
    z = int(zvalue, 2)
    print('Z Value:', zvalue, '=>', z)


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()

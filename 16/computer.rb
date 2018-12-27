class Computer
  attr_reader :registers

  OPCODES = [
    :addr, :addi,
    :mulr, :muli,
    :banr, :bani,
    :borr, :bori,
    :setr, :seti,
    :gtir, :gtri, :gtrr,
    :eqir, :eqri, :eqrr
  ]

  def initialize
    @registers = Array.new(4,0)
  end

  def match_opcodes(before, instructions, after, options = OPCODES)
    before = before.split(',').map { |v| v.to_i }
    instructions = instructions.split(' ').map { |v| v.to_i }
    after = after.split(',').map { |v| v.to_i }
    code, a, b, c = instructions
    #puts ''
    #puts "Searching For Matches: #{after}"
    #puts ''
    options.select do |opcode|
      @registers = before.dup
      #print "#{opcode}: %s - [%s, %s, %s]" %  [@registers, a, b, c]
      send(opcode, a, b, c)
      #puts "= %s" % @registers.inspect
      @registers == after
    end
  end

  def identify_opcodes(before, instructions, after, known_opcodes)
    instr = instructions.split(' ').map { |v| v.to_i }
    code, _ = instr
    #return false if known_opcodes[code]
    options = OPCODES - known_opcodes.values

    opcodes = match_opcodes(before, instructions, after, options)

    if opcodes.length == 1
      opcode = opcodes.first
      known_opcodes[code] = opcode
      return true
    end
    false
  end

  def set_opcodes(opcodes)
    @opcodes = opcodes
  end

  def execute(instruction)
    instr = instruction.split(" ").map &:to_i
    opcode, a, b, c = instr
    opcode = @opcodes[opcode]
    send(opcode, a, b, c)
  end

  def register(r)
    @registers[r]
  end

  def set_register(r,v)
    @registers[r] = v
  end

  def addi(a,b,r)
    @registers[r] = @registers[a] + b
  end

  def addr(a,b,r)
    @registers[r] = @registers[a] + @registers[b]
  end

  def mulr(a,b,r)
    @registers[r] = @registers[a] * @registers[b]
  end

  def muli(a,b,r)
    @registers[r] = @registers[a] * b
  end

  def banr(a,b,r)
    @registers[r] = @registers[a] & @registers[b]
  end

  def bani(a,b,r)
    @registers[r] = @registers[a] & b
  end

  def borr(a,b,r)
    @registers[r] = @registers[a] | @registers[b]
  end

  def bori(a,b,r)
    @registers[r] = @registers[a] | b
  end

  def setr(a,b,r)
    @registers[r] = @registers[a]
  end

  def seti(a,b,r)
    @registers[r] = a
  end

  def gtir(a,b,r)
    @registers[r] = (a > @registers[b]) ? 1:0
  end

  def gtri(a,b,r)
    @registers[r] = (@registers[a] > b) ? 1:0
  end

  def gtrr(a,b,r)
    @registers[r] = (@registers[a] > @registers[b]) ? 1:0
  end

  def eqir(a,b,r)
    @registers[r] = (a == @registers[b]) ? 1:0
  end

  def eqri(a,b,r)
    @registers[r] = (@registers[a] == b) ? 1:0
  end

  def eqrr(a,b,r)
    @registers[r] = (@registers[a] == @registers[b]) ? 1:0
  end
end

class IOPipe 
  @buffer = Channel(Int64).new(2)

  def <<(val)
    @buffer.send(val)
  end

  def shift
    @buffer.receive
  end

  def first
    Channel.receive_first(@buffer)
  end
end

class Puzzle

  property memory = Hash(Int64,Int64).new(0.to_i64)
  property save = {} of Int64 => Int64
  property cursor : Int64
  property relative_base : Int64
  property halted = false

  def initialize
    @cursor = 0.to_i64
    @relative_base = 0.to_i64
  end

  def process(str)
    memory = Hash(Int64,Int64).new(0.to_i64)
    @cursor = 0.to_i64
    str.lines.each do |line|
      parse_codes(line)
    end
  end

  def save_memory
    @save = Hash(Int64,Int64).new(0.to_i64)
    memory.each do |loc, val|
      @save[loc] = val
    end
  end

  def restore_memory
    @memory = Hash(Int64,Int64).new(0.to_i64)
    save.each do |loc, val|
      @memory[loc] = val
    end
  end

  def gencode(code)
    codestr = "%05d" % code
    codes = codestr.split("")
    modes = [] of Int32
    opcode = codes.pop
    opcode = codes.pop + opcode #2Digit Opcode
    opcode = opcode.to_i
    3.times do 
      modes << codes.pop.to_i
    end
    {opcode, modes}
  end

  def fetch_params(count, modes, dest=nil)
    params = [] of Int64
    count.times do |offset|
      arg = memory[@cursor+offset+1]
      val = if modes[offset] == 0
        memory[arg.to_i64]
      elsif modes[offset] == 2
        relloc = @relative_base + arg
        puts "FETCH REL: => #{@relative_base}::#{arg}, #{relloc} #{memory[relloc]}"
        memory[relloc]
      else
        arg
      end
      params << val
      #p "#{offset}, #{params}, #{modes} #{@cursor}, #{memory} (#{arg}:#{val})"
    end
    if dest
      val  = memory[@cursor+dest]
      params << val
      #puts "-> #{dest} (#{params})"
    end
    puts " => #{params}"
    params
  end

  def execute(input = IOPipe.new, output =IOPipe.new)
    @cursor = 0.to_i64
    while true
    #3.times do
      opcode, modes = gencode(memory[@cursor])
      puts "#{opcode}:#{modes}"
      puts "@#{@cursor} => #{opcode}"
      if opcode == 1
        val1, val2, dest = fetch_params(2, modes, 3)
        memory[dest.to_i64] = val1 + val2
        @cursor += 4
      elsif opcode == 2
        val1, val2, dest = fetch_params(2, modes, 3)
        memory[dest.to_i64] = val1 * val2
        @cursor += 4
      elsif opcode == 3
        dest = memory[@cursor+1]
        val = input.shift
        #puts " << #{val}"
        STDOUT.flush
        memory[dest.to_i64] = val
        @cursor += 2
      elsif opcode == 4
        val = fetch_params(1, modes).first
        #puts " >> #{val}"
        output << val
        @cursor += 2
      elsif opcode == 5
        cmp, jmp = fetch_params(2, modes)
        if cmp != 0
          @cursor = jmp.to_i64
        else
          @cursor += 3
        end
      elsif opcode == 6
        cmp, jmp = fetch_params(2, modes)
        if cmp == 0
          @cursor = jmp.to_i64
        else
          @cursor += 3
        end
      elsif opcode == 7
        cmp1, cmp2, dest = fetch_params(2, modes, 3)
        if cmp1 < cmp2
          memory[dest.to_i64] = 1
        else
          memory[dest.to_i64] = 0
        end
        @cursor += 4
      elsif opcode == 8
        cmp1, cmp2, dest = fetch_params(2, modes, 3)
        if cmp1 == cmp2
          memory[dest.to_i64] = 1
        else
          memory[dest.to_i64] = 0
        end
        @cursor += 4
      elsif opcode == 9
        offset = fetch_params(1, modes).first
        puts "RELATIVE --> #{@relative_base} + #{offset}"
        @relative_base += offset
        @cursor += 2
      elsif opcode == 99
        @halted = true
        return output
      else
        puts "Unknown Opcode", opcode
        return output
      end
      #puts "@#{cursor} => #{@memory}"
      #puts "@#{cursor}"
    end
  end

  def parse_codes(line)
    line.split(",").each do |code|
      memory[@cursor] = code.to_i64
      @cursor += 1
    end
  end

  def at(loc)
    memory[loc.to_i64]
  end

  def result
    output = [] of Int64
    input = [1.to_i64]
    execute input, output
    p output
  end

end

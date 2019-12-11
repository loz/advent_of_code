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

class RobotIO
  DIRECTIONS = {
    :N => {
      1 => {1, 0, :E},
      0 => {-1, 0, :W}
    },
    :W => {
      1 => {0, -1, :N},
      0 => {0, 1, :S}
    },
    :E => {
      1 => {0, 1, :S},
      0 => {0, -1, :N}
    },
    :S => {
      1 => {-1, 0, :W},
      0 => {1, 0, :E}
    }
  }
  property panels = {} of Tuple(Int32, Int32) => Int64
  property mode = :paint
  property loc = {0,0}
  property facing = :N

  def color(x,y)
    if panels[{x,y}]?
      panels[{x,y}]
    else
      0.to_i64
    end
  end

  def <<(instruction)
    if mode == :paint
      panels[loc] = instruction.to_i64
      #print "P#{instruction}"
      @mode = :move
    else # :move
      moves = DIRECTIONS[facing][instruction]
      dx, dy, newfacing = moves
      x, y = loc
      x += dx
      y += dy
      @loc = {x, y}
      @facing = newfacing
      #print "M#{instruction}"
      @mode = :paint
    end
  end

  def shift
    x, y = loc
    color(x,y)
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
    puts "#{@cursor} Memory Loaded"
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
    #print "{"
    count.times do |offset|
      arg = memory[@cursor+offset+1]
      #print "#{arg} "
      val = if modes[offset] == 0
        memory[arg.to_i64]
      elsif modes[offset] == 2
        relloc = @relative_base + arg
        #puts "FETCH REL: => #{@relative_base}::#{arg}, #{relloc} #{memory[relloc]}"
        memory[relloc]
      else
        arg
      end
      params << val
      #p "#{offset}, #{params}, #{modes} #{@cursor}, #{memory} (#{arg}:#{val})"
    end
    if dest
      val = if modes[dest-1] == 2
        memory[@cursor+dest] + @relative_base
      else
        memory[@cursor+dest] 
      end
      #print val
      params << val
      #puts "-> #{dest} (#{params})"
    end
    #print "} => #{params} "
    params
  end

  def execute(input = IOPipe.new, output =IOPipe.new)
    @cursor = 0.to_i64
    while true
    #3.times do
      opcode, modes = gencode(memory[@cursor])
      #print "@#{@cursor} [R:#{@relative_base}] => "
      #print "#{opcode}:#{modes} "
      if opcode == 1
        #print "add "
        val1, val2, dest = fetch_params(2, modes, 3)
        #puts "#{val1}, #{val2} -> @#{dest}"
        memory[dest.to_i64] = val1 + val2
        @cursor += 4
      elsif opcode == 2
        #print "mul "
        val1, val2, dest = fetch_params(2, modes, 3)
        #puts "#{val1}, #{val2} -> @#{dest}"
        memory[dest.to_i64] = val1 * val2
        @cursor += 4
      elsif opcode == 3
        #print "inp "
        dest = fetch_params(0, modes, 1).first
        val = input.shift
        #puts "#{val} -> @#{dest}"
        #puts " << #{val}"
        memory[dest.to_i64] = val
        @cursor += 2
      elsif opcode == 4
        #print "out "
        val = fetch_params(1, modes).first
        #puts "#{val}"
        #puts " >> #{val}"
        output << val
        @cursor += 2
      elsif opcode == 5
        #print "jit "
        cmp, jmp = fetch_params(2, modes)
        #puts "#{cmp} :> @#{jmp}"
        if cmp != 0
          @cursor = jmp.to_i64
        else
          @cursor += 3
        end
      elsif opcode == 6
        #print "jif "
        cmp, jmp = fetch_params(2, modes)
        #puts "#{cmp} :> @#{jmp}"
        if cmp == 0
          @cursor = jmp.to_i64
        else
          @cursor += 3
        end
      elsif opcode == 7
        #print "jlt "
        cmp1, cmp2, dest = fetch_params(2, modes, 3)
        #puts "#{cmp1}, #{cmp2} :> @#{dest}"
        if cmp1 < cmp2
          memory[dest.to_i64] = 1
        else
          memory[dest.to_i64] = 0
        end
        @cursor += 4
      elsif opcode == 8
        #print "jie "
        cmp1, cmp2, dest = fetch_params(2, modes, 3)
        #puts "#{cmp1}, #{cmp2} :> @#{dest}"
        if cmp1 == cmp2
          memory[dest.to_i64] = 1
        else
          memory[dest.to_i64] = 0
        end
        @cursor += 4
      elsif opcode == 9
        #print "rad "
        offset = fetch_params(1, modes).first
        #puts "#{offset}"
        #puts "RELATIVE --> #{@relative_base} + #{offset}"
        @relative_base += offset
        @cursor += 2
      elsif opcode == 99
        #puts "hlt "
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
    robot = RobotIO.new
    robot.panels[{0,0}] = 1
    execute robot, robot
    puts "Finished"
    10.times do |y|
      42.times do |x|
        if robot.color(x,y) == 1
          print '#'
        else
          print ' '
        end
      end
      puts
    end
  end

end

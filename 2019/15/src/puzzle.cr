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

class ScreenIO
  property screen = {} of Tuple(Int64,Int64) => Symbol
  property mode = :locx
  property x : Int64
  property y : Int64
  property score : Int64
  property scores = [] of Int64
  property ballx : Int64
  property paddlex : Int64

  TILE = {
    0 => :empty,
    1 => :wall,
    2 => :block,
    3 => :paddle,
    4 => :ball
  }

  CHAR = {
    :empty => ' ',
    :wall => '#',
    :block => '=',
    :paddle => '_',
    :ball => 'O'
  }

  def initialize
    @x = 0.to_i64
    @y = 0.to_i64
    @ballx = 0.to_i64
    @paddlex = 0.to_i64
    @score = 0.to_i64
  end

  def render
    23.times do |y|
      37.times do |x|
        print CHAR[at(x,y)]
      end
      puts
    end
  end

  def shift
    if @paddlex < @ballx
      1.to_i64
    elsif @paddlex > @ballx
      -1.to_i64
    else
      0.to_i64
    end
  end

  def <<(val)
    case @mode
      when :locx
        @x = val
        @mode = :locy
      when :locy
        @y = val
        @mode = :tile
      when :tile
        if @x == -1 && @y == 0
          @score = val
          @scores << val
          #print "\033[1;3f SCORE: #{val} "
        else
          bloc = TILE[val]
          @screen[{@x,@y}] = bloc
          #Render
          #print "\033[#{@y+1};#{@x+1}f#{CHAR[bloc]}"
          @paddlex = x if bloc == :paddle
          if bloc == :ball
            @ballx = x
          end
        end
        @mode = :locx
    end
  end

  def at(x,y)
    @screen[{x,y}]
  end
end

class RepairDroidIO
  @buffer = [] of Int64 #Channel(Int64).new(2)
  property x = 0
  property y = 0
  property ox = 0
  property xy = 0
  property moving = {0,0}
  property moving_dir = :X

  property found = false
  property shortest = [] of Tuple(Symbol, Tuple(Int32, Int32))
  property shortest_len = 0
  property reverting = false

  property visited = [{0,0}]
  property walls = [] of Tuple(Int32,Int32)
  property current_path = [] of Tuple(Symbol, Tuple(Int32, Int32))
  property unexplored = [] of Tuple(Int32, Int32)
  property draw = false

  DIR = {
    :N => {1.to_i64, { 0,-1}},
    :S => {2.to_i64, { 0, 1}},
    :W => {3.to_i64, {-1, 0}},
    :E => {4.to_i64, { 1, 0}}
  }

  OPPOSITE = {
    :N => :S,
    :S => :N,
    :W => :E,
    :E => :W
  }

  def visited?(loc)
    visited.includes?(loc) || walls.includes?(loc)
  end

  def wall?(loc)
    walls.includes?(loc)
  end

  def visit(dir)
    cmd, move = DIR[dir]
    @moving_dir = dir
    @moving = move
    @buffer << cmd
  end

  def revert(move)
    @reverting = true
    dir, _ = move
    visit OPPOSITE[dir]
  end

  def dump_map
    50.times do |y|
      50.times do |x|
        lx = x - 25
        ly = y - 25
        if found && lx == @ox && ly == @oy
          #print "\033[0;32mO"
          print "O"
        elsif lx == @x && ly == @y
          #print "\033[0;32mR"
          print "R"
        elsif lx == 0 && ly == 0
          #print "\033[0;36mS"
          print "S"
        elsif wall?({lx,ly})
          #print "\033[0;31m#"
          print "#"
        elsif visited?({lx,ly})
          #print "\033[0;34m."
          print "."
        elsif unexplored.includes?({lx,ly})
          #print "\033[0;33m?"
          print "?"
        else
          #print "\033[0;37m."
          print " "
        end
      end
      puts
    end
    if found
      puts "R: #{@x},#{@y} O:#{@ox},#{@oy}"
      puts "Best: #{shortest_len}"
    else
      puts "R: #{@x},#{@y}"
    end
  end

  def shift
    if found && unexplored.empty?
      dump_map
      raise "FULLY EXPLORED"
    end
    if @buffer.empty?
      explore_map
    end
    if @buffer.empty?
      p unexplored
      raise "WHAT?"
    end
    @buffer.shift
  end

  def explore_map
    neigbors = fetch_neigbors
    tovisit = neigbors.reject {|n| _, loc = n; visited? loc }
    if tovisit.empty?
      unless current_path.empty?
        lastmove = current_path.pop
        revert(lastmove)
      end
    else
      #Visit the first
      dir, _ = tovisit.pop
      add_to_unexplored(tovisit)
      visit(dir)
    end
  end

  def add_to_unexplored(visits)
    visits.each do |v|
      _, loc = v
      @unexplored << loc
    end
  end

  def fetch_neigbors
    DIR.map do |d, detail|
      _, delta = detail
      dx, dy = delta
      {d, {@x + dx, @y + dy}}
    end
  end

  def <<(status)
    case status
      when 1, 2
        #Accepted and Moved
        dx, dy = @moving
        curloc = {@x, @y}
        @x += dx
        @y += dy
        loc = {@x, @y}
        @visited << loc
        if @reverting
          @reverting = false
        else
          @current_path << {@moving_dir, curloc}
        end
        if status == 2
          @found = true
          @ox = @x
          @oy = @y
          @shortest = @current_path.dup
          @shortest_len = @shortest.size
        end

        @unexplored.delete loc #remove from unexplored
        #puts "#{@moving_dir}. #{loc}, #{found}"
      when 0
        #Failed to Move, but hit a wall
        dx, dy = @moving
        wall = {@x + dx, @y + dy}
        @walls << wall
        @unexplored.delete wall #remove from unexplored
        #puts "#{@moving_dir}#"
    end
    if draw
     #sleep 0.001
     print "\033[0;0f"
     dump_map
    end
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
    droid = RepairDroidIO.new
    #droid.draw = true
    execute(droid, droid)
    p droid.found
    p droid.current_path
  end

end

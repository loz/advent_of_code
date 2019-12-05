class Puzzle

  property memory = [] of Int32
  property save = [] of Int32
  property cursor = 0
  property halted = false

  def process(str)
    memory = [] of Int32
    str.lines.each do |line|
      parse_codes(line)
    end
  end

  def save_memory
    @save = [] of Int32
    memory.each do |code|
      @save << code
    end
  end

  def restore_memory
    @memory = [] of Int32 
    save.each do |code|
      @memory << code
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
    params = [] of Int32
    count.times do |offset|
      arg = memory[@cursor+offset+1]
      val = if modes[offset] == 0
        memory[arg]
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
    params
  end

  def execute(input = [] of Int32)
    output = [] of Int32
    @cursor = 0
    while true
    #3.times do
      opcode, modes = gencode(memory[@cursor])
      #puts "#{opcode}:#{modes}"
      #puts "@#{@cursor} => #{opcode}"
      if opcode == 1
        val1, val2, dest = fetch_params(2, modes, 3)
        #p val1, val2, dest, modes
        memory[dest] = val1 + val2
        @cursor += 4
      elsif opcode == 2
        val1, val2, dest = fetch_params(2, modes, 3)
        memory[dest] = val1 * val2
        @cursor += 4
      elsif opcode == 3
        dest = memory[@cursor+1]
        val = input.shift
        memory[dest] = val
        @cursor += 2
      elsif opcode == 4
        val = fetch_params(1, modes).first
        output << val
        @cursor += 2
      elsif opcode == 5
        cmp, jmp = fetch_params(2, modes)
        if cmp != 0
          @cursor = jmp
        else
          @cursor += 3
        end
      elsif opcode == 6
        cmp, jmp = fetch_params(2, modes)
        if cmp == 0
          @cursor = jmp
        else
          @cursor += 3
        end
      elsif opcode == 7
        cmp1, cmp2, dest = fetch_params(2, modes, 3)
        if cmp1 < cmp2
          memory[dest] = 1
        else
          memory[dest] = 0
        end
        @cursor += 4
      elsif opcode == 8
        cmp1, cmp2, dest = fetch_params(2, modes, 3)
        if cmp1 == cmp2
          memory[dest] = 1
        else
          memory[dest] = 0
        end
        @cursor += 4
      elsif opcode == 99
        @halted = true
        return output
      else
        puts "Unknown Opcode", opcode
        return output
      end
    end
  end

  def parse_codes(line)
    line.split(",").each do |code|
      memory << code.to_i
    end
  end

  def at(loc)
    memory[loc]
  end

  def result
    output = execute [5]
    p output
  end

end

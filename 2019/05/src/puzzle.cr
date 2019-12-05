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

  def execute(input = [] of Int32)
    output = [] of Int32
    @cursor = 0
    while true
    #3.times do
      opcode, modes = gencode(memory[@cursor])
      #puts "#{opcode}:#{modes}"
      #puts "@#{@cursor} => #{opcode}"
      if opcode == 1
        arg1 = memory[@cursor+1]
        arg2 = memory[@cursor+2]
        dest = memory[@cursor+3]
        #puts "-> add #{arg1}(#{memory[arg1]}) + #{arg2}(#{memory[arg2]}) -> #{dest}"
        #puts "-> add #{arg1} + #{arg2} -> #{dest}"
        val1 = if modes[0] == 0
          memory[arg1]
        else
          arg1
        end
        val2 = if modes[1] == 0
          memory[arg2]
        else
          arg2
        end
        memory[dest] = val1 + val2
        @cursor += 4
      elsif opcode == 2
        arg1 = memory[@cursor+1]
        arg2 = memory[@cursor+2]
        dest = memory[@cursor+3]
        #puts "-> mul #{arg1}(#{memory[arg1]}) * #{arg2}(#{memory[arg2]}) -> #{@cursor}"
        #puts "-> mul #{arg1} * #{arg2} -> #{dest}"
        val1 = if modes[0] == 0
          memory[arg1]
        else
          arg1
        end
        val2 = if modes[1] == 0
          memory[arg2]
        else
          arg2
        end
        memory[dest] = val1 * val2
        @cursor += 4
      elsif opcode == 3
        dest = memory[@cursor+1]
        val = input.shift
        memory[dest] = val
        @cursor += 2
      elsif opcode == 4
        arg1 = memory[@cursor+1]
        if modes[0] == 0
          output << memory[arg1]
        else
          output << arg1
        end
        @cursor += 2
      elsif opcode == 5
        arg1 = memory[@cursor+1]
        arg2 = memory[@cursor+2]
        cmp = if modes[0] == 0
          memory[arg1]
        else
          arg1
        end
        jmp = if modes[1] == 0
          memory[arg2]
        else
          arg2
        end
        if cmp != 0
          @cursor = jmp
        else
          @cursor += 3
        end
      elsif opcode == 6
        arg1 = memory[@cursor+1]
        arg2 = memory[@cursor+2]
        cmp = if modes[0] == 0
          memory[arg1]
        else
          arg1
        end
        jmp = if modes[1] == 0
          memory[arg2]
        else
          arg2
        end
        if cmp == 0
          @cursor = jmp
        else
          @cursor += 3
        end
      elsif opcode == 7
        arg1 = memory[@cursor+1]
        arg2 = memory[@cursor+2]
        dest = memory[@cursor+3]
        cmp1 = if modes[0] == 0
          memory[arg1]
        else
          arg1
        end
        cmp2 = if modes[1] == 0
          memory[arg2]
        else
          arg2
        end
        if cmp1 < cmp2
          memory[dest] = 1
        else
          memory[dest] = 0
        end
        @cursor += 4
      elsif opcode == 8
        arg1 = memory[@cursor+1]
        arg2 = memory[@cursor+2]
        dest = memory[@cursor+3]
        cmp1 = if modes[0] == 0
          memory[arg1]
        else
          arg1
        end
        cmp2 = if modes[1] == 0
          memory[arg2]
        else
          arg2
        end
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

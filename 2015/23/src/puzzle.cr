class Puzzle

  @registers = {"a" => 0, "b" => 0} 
  @instructions = [] of String
  @ipointer = 0

  def process(str)
    str.each_line do |line|
      @instructions << line
    end
  end

  def execute
    while @ipointer < @instructions.size
      instruction = @instructions[@ipointer]
      process_line(instruction)
    end
  end

  def process_line(line)
    parts = line.match(/([^\s]+) ([^,]+)(, (.+))*/)
    if parts
      instruction = parts[1]
      case instruction
        when "hlf"
          reg = parts[2]
          @registers[reg] = @registers[reg].tdiv 2
          @ipointer += 1
        when "tpl"
          reg = parts[2]
          @registers[reg] = @registers[reg] * 3
          @ipointer += 1
        when "inc"
          reg = parts[2]
          @registers[reg] += 1
          @ipointer += 1
        when "jmp"
          delta = parts[2].to_i
          @ipointer += delta
        when "jie"
          reg = parts[2]
          val = @registers[reg]
          if val % 2 == 0
            offset = parts[4].to_i
            @ipointer += offset
          else
            @ipointer += 1
          end
        when "jio"
          reg = parts[2]
          val = @registers[reg]
          if val == 1
            offset = parts[4].to_i
            @ipointer += offset
          else
            @ipointer += 1
          end
        else
          p parts
          puts "Unkown Instruction #{instruction}"
          @ipointer += 1
      end
    end
  end

  def set_register(reg, value)
    @registers[reg] = value
  end

  def get_register(reg)
    @registers[reg]
  end

  def result
    @registers["a"] = 1
    execute
    puts @registers
  end

end

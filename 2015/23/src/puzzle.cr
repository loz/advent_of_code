class Puzzle

  @registers = {"a" => 0, "b" => 0} 

  def process(str)
    process_line(str)
  end

  def process_line(line)
    parts = line.match(/(.+) (.+)(, .+)*/)
    if parts
      instruction = parts[1]
      case instruction
        when "hlf"
          reg = parts[2]
          @registers[reg] = @registers[reg].tdiv 2
        when "tpl"
          reg = parts[2]
          @registers[reg] = @registers[reg] * 3
        when "inc"
          reg = parts[2]
          @registers[reg] += 1
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
  end

end

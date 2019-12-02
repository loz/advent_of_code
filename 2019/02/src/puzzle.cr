class Puzzle

  property memory = [] of Int32
  property save = [] of Int32
  property cursor = 0

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

  def execute
    @cursor = 0
    while true
    #3.times do
      opcode = memory[@cursor]
      #puts "@#{@cursor} => #{opcode}"
      if opcode == 1
        arg1 = memory[@cursor+1]
        arg2 = memory[@cursor+2]
        dest = memory[@cursor+3]
        #puts "-> add #{arg1}(#{memory[arg1]}) + #{arg2}(#{memory[arg2]}) -> #{dest}"
        #puts "-> add #{arg1} + #{arg2} -> #{dest}"
        memory[dest] = memory[arg1] + memory[arg2]
      elsif opcode == 2
        arg1 = memory[@cursor+1]
        arg2 = memory[@cursor+2]
        dest = memory[@cursor+3]
        #puts "-> mul #{arg1}(#{memory[arg1]}) * #{arg2}(#{memory[arg2]}) -> #{@cursor}"
        #puts "-> mul #{arg1} * #{arg2} -> #{dest}"
        memory[dest] = memory[arg1] * memory[arg2]
      elsif opcode == 99
        return
      else
        puts "Unknown Opcode", opcode
        return
      end
      @cursor += 4
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
    save_memory
    121.times do |n|
      120.times do |v|
        restore_memory
        noun = n + 1
        verb = v + 1
        memory[1] = noun
        memory[2] = verb
        #print "N:#{noun} V:#{verb}" 
        execute
        result = memory[0]
        #puts "-> #{result}"
        if result == 19690720
          puts "N:#{noun} V:#{verb} -> #{result}"
          res = (100 * noun) + verb
          puts "Result: #{res}"
          return
        end
      end
    end
  end

end

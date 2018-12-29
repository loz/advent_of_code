require_relative '../16/computer'

class Program
  attr_reader :ip_reg, :lines, :machine
  attr_accessor :ip

  def initialize
    @machine = Computer.new(6)
    @ip = 0
  end

  def load(code)
    @lines = []
    code.lines.each do |line|
      if line.start_with?("#ip")
        set_instruction_register(line)
      else
        @lines << parse_instrunction(line)
      end
    end
  end

  def execute(debug = false)
    instr, a, b, c = @lines[@ip]
    @machine.set_register(@ip_reg, @ip)
    if debug
      print "ip=#{@ip} #{@machine.registers.inspect} #{instr} #{a} #{b} #{c} "
    end
    @machine.send(instr, a, b, c)
    @ip = @machine.register(@ip_reg)
    if debug
      puts @machine.registers.inspect
    end
    @ip += 1
  end

  def halted?
    @lines[@ip].nil?
  end

  private

  def set_instruction_register(line)
    _, reg = line.split(" ")
    @ip_reg = reg.to_i
  end

  def parse_instrunction(line)
    instr = line.split(" ")
    [instr[0].to_sym, instr[1].to_i, instr[2].to_i, instr[3].to_i]
  end

end

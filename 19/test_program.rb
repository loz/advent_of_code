require 'minitest/autorun'
require_relative './program'

describe Program do
  before do
    @program = Program.new
    @program.load <<-EOF
#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5
    EOF
  end
 
  it "sets the instruction pointer register" do
    @program.ip_reg.must_equal 0
  end

  it "loads the code lines" do
    @program.lines.length.must_equal 7

    line = @program.lines[3]
    line.must_equal [:addr, 1, 2, 3]
  end

  describe "execute" do
    it "executes the insruction at the current line on the machine" do
      @program.execute

      @program.machine.registers.must_equal [0, 5, 0, 0, 0, 0]
    end

    it "increments the instruction pointer after execution" do
      @program.execute
      @program.ip.must_equal 1
    end

    it "stores the instruction pointer in the ip_reg" do
      2.times { @program.execute }
      
      @program.machine.registers.must_equal [1, 5, 6, 0, 0, 0]
    end

    it "retrieves the value of the instruction pointer from the reg after execution" do
      3.times { @program.execute }
      @program.machine.registers.must_equal [3, 5, 6, 0, 0, 0]
      @program.ip.must_equal 4
    end

    it "halts when there are no more instructions" do
      4.times { @program.execute }
      @program.wont_be :halted?

      @program.execute
      @program.must_be :halted?
    end
  end

end

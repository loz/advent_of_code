require "spec"
require "./spec_helper"

describe Intcode do

  it "supports effectively infinite memory" do
    machine = Intcode.new

    machine.at(12334).should eq 0
  end

  it "executes 1 command to add into memory" do
    machine = Intcode.new
    machine.process("1,0,0,3,99")
    machine.execute

    machine.at(3).should eq 2
  end

  it "executes until halts" do
    machine = Intcode.new
    machine.process("1,0,0,3,1,3,3,7,99")
    machine.execute

    machine.at(7).should eq 4
  end

  it "executes 2 command to multiply into memory" do
    machine = Intcode.new
    machine.process("2,0,0,3,99")
    machine.execute

    machine.at(3).should eq 4
  end

  it "executes 3 commands to store inout value" do
    machine = Intcode.new
    machine.process("3,0,99")
    machine.execute [100.to_i64]

    machine.at(0).should eq 100
  end

  it "executes 4 commands to output value" do
    machine = Intcode.new
    machine.process("3,0,4,0,99")
    out = machine.execute [125.to_i64]
    out.first.should eq 125.to_i64
  end

  it "executes 5 commands to jump-if-true" do
    machine = Intcode.new
    machine.process("1105,1,4,123123123,99")
    machine.execute
    machine.halted.should eq true
  end

  it "executes 6 commands to jump-if-false" do
    machine = Intcode.new
    machine.process("1106,0,4,123123123,99")
    machine.execute
    machine.halted.should eq true
  end

  it "executes 7 commands to less than to 1" do
    machine = Intcode.new
    machine.process("11107,2,4,0,99")
    machine.execute
    machine.at(0).should eq 1
  end

  it "executes 7 commands to gt than to 0" do
    machine = Intcode.new
    machine.process("11107,4,2,0,99")
    machine.execute
    machine.at(0).should eq 0
  end

  it "executes 8 commands to equals to 1" do
    machine = Intcode.new
    machine.process("11108,2,2,0,99")
    machine.execute
    machine.at(0).should eq 1
  end

  it "executes 8 commands to equals to 0" do
    machine = Intcode.new
    machine.process("11108,4,2,0,99")
    machine.execute
    machine.at(0).should eq 0
  end

  it "supports parameter modes for instructions" do
    machine = Intcode.new
    machine.process("1002,4,3,4,33")
    machine.execute
    machine.at(4).should eq 99
  end

  it "supports relative mode" do
    machine = Intcode.new
    machine.process("109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99")
    output = [] of Int64
    machine.execute output, output

    machine.halted.should eq true
    output.should eq [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
  end

  it "supports large numbers" do
    machine = Intcode.new
    machine.process("1102,34915192,34915192,7,4,7,99,0")
    output = [] of Int64
    machine.execute output, output
    output.first.to_s.size.should eq 16
  end

  it "supports other large numbers" do
    machine = Intcode.new
    machine.process("104,1125899906842624,99")
    output = [] of Int64
    machine.execute output, output
    output.first.should eq 1125899906842624
  end
  it "supports large numbers" do
    machine = Intcode.new
    machine.process("1102,34915192,34915192,7,4,7,99,0")
    output = [] of Int64
    machine.execute output, output
    output.first.to_s.size.should eq 16
  end
end

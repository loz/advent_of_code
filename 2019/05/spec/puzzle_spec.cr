require "spec"
require "./spec_helper"

describe Puzzle do

  it "executes 1 command to add into memory" do
    puzzle = Puzzle.new
    puzzle.process("1,0,0,3,99")
    puzzle.execute

    puzzle.at(3).should eq 2
  end

  it "executes until halts" do
    puzzle = Puzzle.new
    puzzle.process("1,0,0,3,1,3,3,7,99")
    puzzle.execute

    puzzle.at(7).should eq 4
  end

  it "executes 2 command to multiply into memory" do
    puzzle = Puzzle.new
    puzzle.process("2,0,0,3,99")
    puzzle.execute

    puzzle.at(3).should eq 4
  end

  it "executes 3 commands to store inout value" do
    puzzle = Puzzle.new
    puzzle.process("3,0,99")
    puzzle.execute [100]

    puzzle.at(0).should eq 100
  end

  it "executes 4 commands to output value" do
    puzzle = Puzzle.new
    puzzle.process("3,0,4,0,99")
    out = puzzle.execute [125]
    out.first.should eq 125
  end

  it "executes 5 commands to jump-if-true" do
    puzzle = Puzzle.new
    puzzle.process("1105,1,4,123123123,99")
    puzzle.execute
    puzzle.halted.should eq true
  end

  it "executes 6 commands to jump-if-false" do
    puzzle = Puzzle.new
    puzzle.process("1106,0,4,123123123,99")
    puzzle.execute
    puzzle.halted.should eq true
  end

  it "executes 7 commands to less than to 1" do
    puzzle = Puzzle.new
    puzzle.process("11107,2,4,0,99")
    puzzle.execute
    puzzle.at(0).should eq 1
  end

  it "executes 7 commands to gt than to 0" do
    puzzle = Puzzle.new
    puzzle.process("11107,4,2,0,99")
    puzzle.execute
    puzzle.at(0).should eq 0
  end

  it "executes 8 commands to equals to 1" do
    puzzle = Puzzle.new
    puzzle.process("11108,2,2,0,99")
    puzzle.execute
    puzzle.at(0).should eq 1
  end

  it "executes 8 commands to equals to 0" do
    puzzle = Puzzle.new
    puzzle.process("11108,4,2,0,99")
    puzzle.execute
    puzzle.at(0).should eq 0
  end

  it "supports parameter modes for instructions" do
    puzzle = Puzzle.new
    puzzle.process("1002,4,3,4,33")
    puzzle.execute
    puzzle.at(4).should eq 99
  end
end

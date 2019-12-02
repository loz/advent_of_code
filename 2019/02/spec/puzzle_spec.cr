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
end

require "spec"
require "./spec_helper"

describe Puzzle do

  it "finds symbols for U/L" do
    puzzle = Puzzle.new
    puzzle.process("RRL")
    puzzle.code.should eq ['6']
  end

  it "finds symbols for D/R" do
    puzzle = Puzzle.new
    puzzle.process("RRDR")
    puzzle.code.should eq ['C']
  end

  it "ignores illegal moves" do
    puzzle = Puzzle.new
    puzzle.process("UUDDLLRRRRRRRR")
    puzzle.code.should eq ['9']
  end

  it "processes code from end of previous lines" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    ULL
    RRDDD
    LURDL
    UUUUD
    EOF

    puzzle.code.should eq ['5', 'D', 'B', '3']
  end
end

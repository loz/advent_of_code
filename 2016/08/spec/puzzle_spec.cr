require "spec"
require "./spec_helper"

describe Puzzle do

  it "can process a rect command" do
    puzzle = Puzzle.new
    puzzle.process("rect 8x4")

    puzzle.on?(0,0).should eq true
    puzzle.on?(3,3).should eq true
    puzzle.on?(7,3).should eq true
    puzzle.on?(10,3).should eq false
  end

  it "can process a rotate row command" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    rect 2x2
    rotate row y=0 by 2
    EOF

    puzzle.on?(0,0).should eq false
    puzzle.on?(0,1).should eq true
    puzzle.on?(2,0).should eq true
  end

  it "can process a rotate column command" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    rect 2x2
    rotate column x=1 by 3
    EOF

    puzzle.on?(1,0).should eq false
    puzzle.on?(1,2).should eq false
    puzzle.on?(1,3).should eq true
    puzzle.on?(1,4).should eq true

  end
end

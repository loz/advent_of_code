require "spec"
require "./spec_helper"

describe Puzzle do

  it "supports going Right" do
    puzzle = Puzzle.new
    puzzle.process("R2")

    puzzle.orientation.should eq "E"
    puzzle.location.should eq({2,0})
  end

  it "supports going Left" do
    puzzle = Puzzle.new
    puzzle.process("L2")

    puzzle.orientation.should eq "W"
    puzzle.location.should eq({-2,0})
  end

  it "supports going Left Twice" do
    puzzle = Puzzle.new
    puzzle.process("L2, L2")

    puzzle.orientation.should eq "S"
    puzzle.location.should eq({-2,2})
  end

  it "supports going Right Twice" do
    puzzle = Puzzle.new
    puzzle.process("R2, R10")

    puzzle.orientation.should eq "S"
    puzzle.location.should eq({2,10})
  end

  it "supports going Right + Left" do
    puzzle = Puzzle.new
    puzzle.process("R2, L10")

    puzzle.orientation.should eq "N"
    puzzle.location.should eq({2,-10})
  end

  it "supports going Left + Right" do
    puzzle = Puzzle.new
    puzzle.process("L4, R7")

    puzzle.orientation.should eq "N"
    puzzle.location.should eq({-4,-7})
  end

  it "supports going Left + Left + Right" do
    puzzle = Puzzle.new
    puzzle.process("L4, L7, R5")

    puzzle.orientation.should eq "W"
    puzzle.location.should eq({-9,7})
  end

  it "supports going Left + Left + Left" do
    puzzle = Puzzle.new
    puzzle.process("L4, L7, L3")

    puzzle.orientation.should eq "E"
    puzzle.location.should eq({-1,7})
  end
end

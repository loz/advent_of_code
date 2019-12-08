require "spec"
require "./spec_helper"

describe Puzzle do

  it "generates permutations of parcels" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    1
    2
    3
    4
    5
    EOF

    permutations = puzzle.permutations

    permutations.should contain({[1,4], [2,3], [5]})
  end

  it "can determine a valid configuration" do
    puzzle = Puzzle.new
    puzzle.valid?({[5], [1,4], [3,2]}).should eq true
  end

  it "can determine an invalid configuration" do
    puzzle = Puzzle.new
    puzzle.valid?({[6], [1,4], [3,2]}).should eq false
  end

  it "can select the smallest group package wise" do
    puzzle = Puzzle.new
    puzzle.passenger({[6], [1,4], [3,2]}).should eq [6]
  end

  it "can caluclate the QE for a present group" do
    puzzle = Puzzle.new

    puzzle.qe([11, 9]).should eq 99
    puzzle.qe([10, 7, 3]).should eq 210
    puzzle.qe([9, 8, 3]).should eq 216
  end
end

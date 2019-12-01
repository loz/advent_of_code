require "spec"
require "./spec_helper"

describe Puzzle do

  it "calculates fuel for multiple of 3" do
    puzzle = Puzzle.new
    puzzle.fuel(12).should eq 2
  end

  it "calculates fuel rounding down" do
    puzzle = Puzzle.new
    puzzle.fuel(17).should eq 3
  end

  it "calculates fuel for the fuel" do
    puzzle = Puzzle.new
    puzzle.fuel(1969).should eq (654 + 216 + 70 + 21 + 5)
  end
end

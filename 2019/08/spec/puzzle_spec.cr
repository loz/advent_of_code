require "spec"
require "./spec_helper"

describe Puzzle do

  it "counts given digit in a layer" do
    puzzle = Puzzle.new
    puzzle.process("112213334445", 3, 2)
    layer = puzzle.layers.first
    puzzle.count_digit(1, layer).should eq 3
    puzzle.count_digit(2, layer).should eq 2
  end

  it "can merge layer on top of a layer to produce a composite layer" do
    puzzle = Puzzle.new
    layer1 = "0222"
    layer2 = "1122"

    newlayer = puzzle.compose(layer1, layer2)
    newlayer.should eq "0122"
  end
end

require "spec"
require "./spec_helper"

describe Puzzle do

  it "does not decompress with mo markers" do
    puzzle = Puzzle.new

    puzzle.decompress("ADVENT").should eq "ADVENT"
  end

  it "decompresses chunks according to ()" do
    puzzle = Puzzle.new

    puzzle.decompress("A(1x5)BC").should eq "ABBBBBC"
  end

  it "decompresses () in repeat correctly" do
    puzzle = Puzzle.new

    puzzle.decompress("X(8x2)(3x3)ABCY").should eq "X(3x3)ABC(3x3)ABCY"
  end

  it "calculates the lengths using v2" do
    puzzle = Puzzle.new

    puzzle.v2length("(3x3)XYZ").should eq 9

    puzzle.v2length("X(8x2)(3x3)ABCY").should eq 20

    puzzle.v2length("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN").should eq 445

    puzzle.v2length("(27x12)(20x12)(13x14)(7x10)(1x12)A").should eq 241920
  end
end

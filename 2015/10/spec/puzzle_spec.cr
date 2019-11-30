require "spec"
require "./spec_helper"

describe Puzzle do

  it "counts 1 digit" do
    puzzle = Puzzle.new
    puzzle.looksay("1").should eq "11"
    puzzle.looksay("6").should eq "16"
  end

  it "counts 2 digits" do
    puzzle = Puzzle.new
    puzzle.looksay("11").should eq "21"
    puzzle.looksay("66").should eq "26"
  end

  it "counts multiple" do
    puzzle = Puzzle.new
    puzzle.looksay("111221").should eq "312211"
  end
end

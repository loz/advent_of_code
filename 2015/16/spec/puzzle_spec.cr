require "spec"
require "./spec_helper"

describe Puzzle do

  it "matches if only children match" do
    puzzle = Puzzle.new
    result, _ = puzzle.match("Sue 1: children: 3")
    result.should eq true
  end

  it "doesnt match if children don't match" do
    puzzle = Puzzle.new
    result, _ = puzzle.match("Sue 1: children: 2, cats: 7")
    result.should eq false
  end

  it "returns name" do
    puzzle = Puzzle.new
    _, name= puzzle.match("Sue 1: children: 2, cats: 7")
    name.should eq "Sue 1"
  end
end

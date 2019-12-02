require "spec"
require "./spec_helper"

describe Puzzle do

  it "calculates presents for house 1" do
    puzzle = Puzzle.new
    puzzle.presents(1).should eq 10
  end

  it "calculates presents for house 2" do
    puzzle = Puzzle.new
    puzzle.presents(2).should eq 30
  end

  it "calculates presents for house 9" do
    puzzle = Puzzle.new
    puzzle.presents(9).should eq 130
  end

end

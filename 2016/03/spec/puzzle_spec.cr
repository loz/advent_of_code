require "spec"
require "./spec_helper"

describe Puzzle do

  it "can detect a valid triangle" do
    puzzle = Puzzle.new
    puzzle.valid?({3,4,5}).should eq true
  end

  it "can detect an invalid triangle" do
    puzzle = Puzzle.new

    puzzle.reslice
    
    puzzle.valid?({5,10,25}).should eq false
  end
end

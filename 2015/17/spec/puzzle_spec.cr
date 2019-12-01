require "spec"
require "./spec_helper"

describe Puzzle do

  it "calculates options for volume" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    20
    15
    10
    5
    5
    EOF
    
    perms = puzzle.options(25)
    perms.should contain [20,5]
    perms.should contain [15,10]
    perms.should contain [15, 5, 5]
  end
end

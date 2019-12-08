require "spec"
require "./spec_helper"

describe Puzzle do

  it "can calculate N for x,y" do
    puzzle = Puzzle.new

    puzzle.n(3,4).should eq 18
    puzzle.n(6,1).should eq 21
    puzzle.n(2,5).should eq 17
  end

  it "can calculate Nth code" do
    puzzle = Puzzle.new

    puzzle.nth(1).should eq 20151125
    puzzle.nth(21).should eq 33511524
    puzzle.nth(9).should eq 16929656
    puzzle.nth(17).should eq 17552253
  end
end

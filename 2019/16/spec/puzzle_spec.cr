require "spec"
require "./spec_helper"

describe Puzzle do

  it "caclulates the sum digit for a set of digits (1 index)" do
    puzzle = Puzzle.new
    puzzle.sumof([1,2,3,4], 1).should eq 2  #(1 + 0 + -3 + 0)

    puzzle.sumof([1,2,3,4,5,6,7,8], 5).should eq 6
  end

  it "calculates the new digits from input digits" do
    puzzle = Puzzle.new

    digits = puzzle.fft([0,3,4,1,5,5,1,8])
    digits.should eq [0,1,0,2,9,4,9,8]
  end

  pending "calculates sum with n repetitions" do
    #When repeating, before modding, it will be
    #d1,d2,d3....  will repeat up to 4 * digits 
    # from here we have a set of repeating combos (d1 * 1, d2 * 0,...)
    # so just * x where x wil give you the number
  end
end

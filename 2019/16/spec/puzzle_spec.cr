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

  it "can calculate offset version" do
    puzzle = Puzzle.new

    offset = 10
    repeat = 3

    input = [2,5,6,7,2,4,5,2,9]
    slow = input * repeat

    #puts "==== SLOW ==="
    #puts slow
    10.times do
      slow = puzzle.fft(slow)
      #p slow
    end

    fast = input * repeat
    fast = fast[offset, fast.size]

    #puts "==== FAST ==="
    #puts fast
    10.times do
      fast = puzzle.offset_fft(offset, fast)
      #p fast
    end
    offset_slow = slow[offset,10]
    offset_fast = fast[0,10]
    offset_fast.should eq offset_slow
  end
end

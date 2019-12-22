require "spec"
require "./spec_helper"

describe Puzzle do

  describe "deal into new stack" do
    it "reverses the deck" do
      puzzle = Puzzle.new
      puzzle.deck = (0...10).to_a
      puzzle.deal_new_stack
      puzzle.deck.should eq [9,8,7,6,5,4,3,2,1,0]
    end
  end

  describe "cut N" do
    it "cuts the deck at N cards" do
      puzzle = Puzzle.new
      puzzle.deck = (0...10).to_a
      puzzle.cut(4)
      puzzle.deck.should eq [4,5,6,7,8,9,0,1,2,3]
    end

    it "cuts with -ve N" do
      puzzle = Puzzle.new
      puzzle.deck = (0...10).to_a
      puzzle.cut(-3)
      puzzle.deck.should eq [7,8,9,0,1,2,3,4,5,6]
    end
  end

  describe "deal with increment N" do
    it "deals out card every n spaces, looping round" do
      puzzle = Puzzle.new
      puzzle.deck = (0...10).to_a
      puzzle.deal_with_increment(3)
      puzzle.deck.should eq [0,7,4,1,8,5,2,9,6,3]
    end
  end
  
  it "can process set of rules" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    deal with increment 7
    deal into new stack
    deal into new stack
    EOF

    puzzle.deck = (0...10).to_a
    puzzle.shuffle
    puzzle.deck.should eq [0,3,6,9,2,5,8,1,4,7]
  end

  it "can process example 2" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    cut 6
    deal with increment 7
    deal into new stack
    EOF

    puzzle.deck = (0...10).to_a
    puzzle.shuffle
    puzzle.deck.should eq [3,0,7,4,1,8,5,2,9,6]
  end

  it "can process example 3" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    deal with increment 7
    deal with increment 9
    cut -2
    EOF

    puzzle.deck = (0...10).to_a
    puzzle.shuffle
    puzzle.deck.should eq [6,3,0,7,4,1,8,5,2,9]
  end

  it "can process example 4" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    deal into new stack
    cut -2
    deal with increment 7
    cut 8
    cut -4
    deal with increment 7
    cut 3
    deal with increment 9
    deal with increment 3
    cut -1
    EOF

    puzzle.deck = (0...10).to_a
    puzzle.shuffle
    puzzle.deck.should eq [9,2,5,8,1,4,7,0,3,6]
  end
end

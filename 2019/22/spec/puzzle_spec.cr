require "spec"
require "./spec_helper"

describe Puzzle do

  describe "deal into new stack" do
    it "reverses the deck" do
      puzzle = Puzzle.new
      puzzle.deck = (0...10).to_a.map {|n| n.to_i64}
      puzzle.deal_new_stack
      puzzle.deck.should eq [9,8,7,6,5,4,3,2,1,0]
    end

    it "can determine what position nth position came from" do
      puzzle = Puzzle.new

      original = (0...10).to_a.map {|n| n.to_i64}

      puzzle.deck = original.dup
      puzzle.deal_new_stack

      (0...10).each do |n|
        odigit = puzzle.reverse_digit_deal_new_stack(n)
        digit = puzzle.deck[n]
        digit.should eq original[odigit]
      end
    end
  end

  describe "cut N" do
    it "cuts the deck at N cards" do
      puzzle = Puzzle.new
      puzzle.deck = (0...10).to_a.map {|n| n.to_i64}
      puzzle.cut(4)
      puzzle.deck.should eq [4,5,6,7,8,9,0,1,2,3]
    end

    it "cuts with -ve N" do
      puzzle = Puzzle.new
      puzzle.deck = (0...10).to_a.map {|n| n.to_i64}
      puzzle.cut(-3)
      puzzle.deck.should eq [7,8,9,0,1,2,3,4,5,6]
    end

    it "calculates nth card cutting N" do
      puzzle = Puzzle.new

      original = (0...10).to_a.map {|n| n.to_i64}

      puzzle.deck = original.dup
      puzzle.cut(4)

      (0...10).each do |n|
        odigit = puzzle.reverse_digit_cut(4, n)
        digit = puzzle.deck[n]
        digit.should eq original[odigit]
      end
    end

    it "calculates nth card cutting -N" do
      puzzle = Puzzle.new

      original = (0...10).to_a.map {|n| n.to_i64}
      
      puzzle.deck = original.dup
      puzzle.cut(-3)

      (0...10).each do |n|
        odigit = puzzle.reverse_digit_cut(-3, n)
        digit = puzzle.deck[n]
        digit.should eq original[odigit]
      end
    end

  end

  describe "deal with increment N" do
    it "deals out card every n spaces, looping round" do
      puzzle = Puzzle.new
      puzzle.deck = (0...10).to_a.map {|n| n.to_i64}
      puzzle.deal_with_increment(3)
      puzzle.deck.should eq [0,7,4,1,8,5,2,9,6,3]

      puzzle.deck = (0...10).to_a.map {|n| n.to_i64}
      puzzle.deal_with_increment(9)
      puzzle.deck.should eq [0,9,8,7,6,5,4,3,2,1]
    end

    it "calculates nth card with increment N" do
      puzzle = Puzzle.new
      original = (0...10).to_a.map {|n| n.to_i64}

      puzzle.deck = original.dup
      puzzle.deal_with_increment(3)

      (0...10).each do |n|
        odigit = puzzle.reverse_digit_deal_with_increment(3, n)
        digit = puzzle.deck[n]
        digit.should eq original[odigit]
      end
    end

    it "works for bug #1 (inc 9)" do
      puzzle = Puzzle.new

      puzzle.deck = (0...10).to_a.map {|n| n.to_i64}
      puzzle.deal_with_increment(9)

      original = [2, 3, 4, 5, 6, 7, 8, 9, 0, 1].map {|i| i.to_i64}

      puzzle.deck = original.dup
      puzzle.deal_with_increment(9)

      (0...10).each do |n|
        odigit = puzzle.reverse_digit_deal_with_increment(9, n)
        digit = puzzle.deck[n]
        digit.should eq original[odigit]
      end
    end

    it "works for bug #2 (inc 7)" do
      puzzle = Puzzle.new

      puzzle.deck = (0...10).to_a.map {|n| n.to_i64}
      puzzle.deal_with_increment(7)

      original = [2, 3, 4, 5, 6, 7, 8, 9, 0, 1].map {|i| i.to_i64}

      puzzle.deck = original.dup
      puzzle.deal_with_increment(7)

      (0...10).each do |n|
        odigit = puzzle.reverse_digit_deal_with_increment(7, n)
        digit = puzzle.deck[n]
        digit.should eq original[odigit]
      end
    end
  end
  
  it "can process set of rules" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    deal with increment 7
    deal into new stack
    deal into new stack
    EOF

    puzzle.deck = (0...10).to_a.map {|n| n.to_i64}
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

    puzzle.deck = (0...10).to_a.map {|n| n.to_i64}
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

    puzzle.deck = (0...10).to_a.map {|n| n.to_i64}
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

    puzzle.deck = (0...10).to_a.map {|n| n.to_i64}
    puzzle.shuffle
    puzzle.deck.should eq [9,2,5,8,1,4,7,0,3,6]
  end

  it "can calculate a single card destination for a shuffle" do
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

    original = (0...10).to_a.map {|n| n.to_i64}

    puzzle.deck = original.dup
    puzzle.shuffle

    rev = (0...10).map do |n|
      digit = puzzle.calculate(n)
      original[digit]
    end
    
    rev.should eq puzzle.deck
  end
end

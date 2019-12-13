require "spec"
require "./spec_helper"

describe Puzzle do

  it "considers ABBA string tls" do
    puzzle = Puzzle.new

    puzzle.tls?("abba[mnop]qrst").should eq true
  end

  it "does not consider ABBA in [] tls" do
    puzzle = Puzzle.new

    puzzle.tls?("abcd[bddb]xyyx").should eq false
  end

  it "does not consider AAAA string tls" do
    puzzle = Puzzle.new

    puzzle.tls?("aaaa[qwer]tyui").should eq false
  end

  it "doe  consider AAAA with another ABBA string tls" do
    puzzle = Puzzle.new

    puzzle.tls?("aaaa[qwer]tyuixyyxqwert").should eq true
  end
end

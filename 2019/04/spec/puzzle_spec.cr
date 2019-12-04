require "spec"
require "./spec_helper"

describe Puzzle do

  it "112233 is valid" do
    puzzle = Puzzle.new
    puzzle.valid("112233").should eq true
  end

  it "101111 is not valid" do
    puzzle = Puzzle.new
    puzzle.valid("101111").should eq false
  end

  it "123444 is not valid" do
    puzzle = Puzzle.new
    puzzle.valid("123444").should eq false
  end

  it "111122 is valid" do
    puzzle = Puzzle.new
    puzzle.valid("111122").should eq true
  end
end

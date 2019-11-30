require "spec"
require "./spec_helper"

describe Puzzle do

  it "counts arrays of numbers" do
    puzzle = Puzzle.new
    puzzle.process("[1,2,3]")

    puzzle.sum.should eq 6
  end

  it "counts has values of numbers" do
    puzzle = Puzzle.new
    puzzle.process(%[{"a":{"b":4},"c":-1}])

    puzzle.sum.should eq 3
  end

  it "counts cross multiple lines" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    [[1,2,3],
    [],
    {"a":[-1,1]},
    {"a":2,"b":4}]
    EOF

    puzzle.sum.should eq 12
  end

  it "counts red val hash as 0" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    [1,{"c":"red","b":2},3]
    EOF

    puzzle.sum.should eq 4
  end
end

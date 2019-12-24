require "spec"
require "./spec_helper"

describe Puzzle do

  it "dies if not 1 bug adjacent" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    #....
    .....
    .....
    .....
    .....
    EOF

    puzzle.at(0,0).should eq '#'
    puzzle.generation
    puzzle.at(0,0).should eq '.'
  end

  it "lives if 1 bug adjacent" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    #....
    #....
    .....
    .....
    .....
    EOF

    puzzle.at(0,0).should eq '#'
    puzzle.generation
    puzzle.at(0,0).should eq '#'
  end

  it "infests empty if 1 or 2 bugs adjacent" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    ##...
    #....
    .....
    ...#.
    .....
    EOF

    puzzle.generation
    puzzle.at(0,0).should eq '.'
    puzzle.at(1,1).should eq '#'
    puzzle.at(3,3).should eq '.'
    puzzle.at(2,3).should eq '#'
    puzzle.at(4,3).should eq '#'
    puzzle.at(3,2).should eq '#'
    puzzle.at(3,4).should eq '#'
  end

  it "matches example" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    ....#
    #..#.
    #..##
    ..#..
    #....
    EOF
    puzzle.generation
    puzzle.dump.should eq <<-EOF
    #..#.
    ####.
    ###.#
    ##.##
    .##..
    EOF
  end

  it "calculates biodiversity rating" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    ....#
    #..#.
    .....
    #....
    .#...
    EOF

    puzzle.diversity.should eq 16 + 32 + 256 + 32768 + 2097152
  end
end

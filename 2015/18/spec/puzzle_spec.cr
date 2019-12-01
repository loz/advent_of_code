require "spec"
require "./spec_helper"

describe Puzzle do

  it "generates the next version" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    .#.#.#
    ...##.
    #....#
    ..#...
    #.#..#
    ####..
    EOF

    newone = puzzle.generate
    newone.should eq <<-EOF
    #.##.#
    ####.#
    ...##.
    ......
    #...#.
    #.####
    EOF
  end

  it "generates for multiple generations" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    .#.#.#
    ...##.
    #....#
    ..#...
    #.#..#
    ####..
    EOF

    4.times { puzzle.generate }
    puzzle.current.should eq <<-EOF
    #.####
    #....#
    ...#..
    .##...
    #.....
    #.#..#
    EOF
  end

  it "counts on lights" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    .#.#.#
    ...##.
    #....#
    ..#...
    #.#..#
    ####..
    EOF

    puzzle.onlights.should eq 17
  end
end

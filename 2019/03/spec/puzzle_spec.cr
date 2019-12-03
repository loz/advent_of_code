require "spec"
require "./spec_helper"

describe Puzzle do

  it "calculates bounds for a sequence" do
    puzzle = Puzzle.new
    
    bounds = puzzle.bounds("R10,D10,L20,U20")
    bounds.should eq({-10,-10,10,10})
  end

  it "plot wires into grid" do
    puzzle = Puzzle.new
    
    puzzle.process("R5,D5,L7,U8\nU0")

    puzzle.to_s.should eq <<-EOF
    1.......
    1.......
    1.......
    1.o11111
    1......1
    1......1
    1......1
    1......1
    11111111
    EOF
  end

  it "plot intersections into grid" do
    puzzle = Puzzle.new
    
    puzzle.process <<-EOF
    R5,D5,L7,U8
    U2,R3,D5,R4
    EOF

    puzzle.to_s.should eq <<-EOF
    1.........
    1.2222....
    1.2..2....
    1.o11X11..
    1....2.1..
    1....2.1..
    1....22X22
    1......1..
    11111111..
    EOF
  end

  it "locates intersections" do
    puzzle = Puzzle.new
    
    puzzle.process <<-EOF
    R5,D5,L7,U8
    U2,R3,D5,R4
    EOF

    joins = puzzle.intersections
    joins.size.should eq 2
    joins.should contain({3,0})
    joins.should contain({5,-3})
  end

  it "calculates closest intersection" do
    puzzle = Puzzle.new
    
    puzzle.process <<-EOF
    R5,D5,L7,U8
    U2,R3,D5,R4
    EOF

    closest = puzzle.closest_intersection
    closest.should eq({3,0})
  end

  it "calculates distance for example 1" do
    puzzle = Puzzle.new
    
    puzzle.process <<-EOF
    R8,U5,L5,D3
    U7,R6,D4,L4
    EOF

    closest = puzzle.closest_intersection
    puzzle.distance_to(closest).should eq 6

  end

  it "calculates distance for example 1" do
    puzzle = Puzzle.new
    
    puzzle.process <<-EOF
    R75,D30,R83,U83,L12,D49,R71,U7,L72
    U62,R66,U55,R34,D71,R55,D58,R83
    EOF

    closest = puzzle.closest_intersection
    puzzle.distance_to(closest).should eq 159

  end

  it "calculates steps to intersection" do
    puzzle = Puzzle.new
    
    puzzle.process <<-EOF
    R8,U5,L5,D3
    U7,R6,D4,L4
    EOF

    intersections = puzzle.intersections

    steps = puzzle.steps_to(intersections[0])
    steps["1"].should eq 15
    steps["2"].should eq 15

    steps = puzzle.steps_to(intersections[1])
    steps["1"].should eq 20
    steps["2"].should eq 20

  end
end

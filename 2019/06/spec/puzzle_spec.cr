require "spec"
require "./spec_helper"

describe Puzzle do

  it "builds a tree of orbits" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    C)D
    B)C
    C)E
    COM)A
    A)B
    EOF

    planet = puzzle.planet("C")
    planet.parent.try {|p| p.name }.should eq "B"
    children = planet.children.map { |p| p.name}
    children.should contain "D"
    children.should contain "E"
  end

  it "can calculate total orbits" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    C)D
    B)C
    C)E
    COM)A
    A)B
    EOF

    root = puzzle.planet("COM")
    puzzle.orbits(root).should eq (1 + 2 + 3 + 4 + 4)
  end
end

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

  it "can calculate ancestors" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    C)D
    B)C
    C)E
    COM)A
    A)B
    EOF

    planet = puzzle.planet("D")
    puzzle.ancestors(planet).should eq ["C", "B", "A", "COM"]
  end

  it "can calculate common ancestors" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    COM)B
    B)C
    C)D
    D)E
    E)F
    B)G
    G)H
    D)I
    E)J
    J)K
    K)L
    K)YOU
    I)SAN
    EOF

    one = puzzle.planet("YOU")
    two = puzzle.planet("SAN")
    common, distance = puzzle.common_ancestor(one, two)
    common.should eq "D"
    distance.should eq 4
  end
end

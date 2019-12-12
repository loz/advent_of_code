require "spec"
require "./spec_helper"

describe Puzzle do

  it "can calculate effect of gravity" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    <x=-1, y=0, z=2>
    <x=2, y=-10, z=-7>
    <x=4, y=-8, z=8>
    <x=3, y=5, z=-1>
    EOF

    puzzle.step

    vels = puzzle.moons.map {|m| _, v = m; v}
    vels.should contain({ 3,-1,-1})
    vels.should contain({ 1, 3, 3})
    vels.should contain({-3, 1,-3})
    vels.should contain({-1,-3, 1})
  end

  it "can calculate effect of velocity" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    <x=-1, y=0, z=2>
    <x=2, y=-10, z=-7>
    <x=4, y=-8, z=8>
    <x=3, y=5, z=-1>
    EOF

    puzzle.step
    #puzzle.moons.each {|m| p m }

    locs = puzzle.moons.map {|m| l, _ = m; l}
    locs.should contain({ 2, -1, 1})
    locs.should contain({ 3, -7,-4})
    locs.should contain({ 1, -7, 5})
    locs.should contain({ 2,  2, 0})
  end

  it "can calculate energy for a moon" do
    puzzle = Puzzle.new

    puzzle.energy({({2,1,-3}),({-3,-2,1})}).should eq 36
    puzzle.energy({({3,-6, 1}),({3,2,-3})}).should eq 80
  end
end

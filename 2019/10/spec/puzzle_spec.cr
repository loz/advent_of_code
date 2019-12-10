require "spec"
require "./spec_helper"

describe Puzzle do

  it "calculates points between src and dest sectors" do
    puzzle = Puzzle.new

    locations = puzzle.points_between({0,0}, {3,0})
    locations.should eq [{1,0}, {2,0}]

    locations = puzzle.points_between({0,0}, {0,4})
    locations.should eq [{0,1}, {0,2}, {0,3}]

    locations = puzzle.points_between({0,0}, {4,4})
    locations.should eq [{1,1}, {2,2}, {3,3}]

    locations = puzzle.points_between({0,0}, {9,6})
    locations.should eq [{3,2}, {6,4}]

    locations = puzzle.points_between({0,0}, {4,8})
    locations.should eq [{1,2}, {2,4}, {3,6}]

    locations = puzzle.points_between({3,4}, {1,0})
    locations.should eq [{2,2}]

  end

  it "loads locations of asteroids" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    .#..#
    .....
    #####
    ....#
    ...##
    EOF

    rocks = puzzle.asteroids
    rocks.size.should eq 10
    rocks.should contain({1,0})
    rocks.should contain({4,0})
    rocks.should contain({0,2})
    rocks.should contain({1,2})
    rocks.should contain({2,2})
    rocks.should contain({3,2})
    rocks.should contain({4,2})
    rocks.should contain({4,3})
    rocks.should contain({3,4})
    rocks.should contain({4,4})
  end

  it "can calculate line of sight" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    .#..#
    .....
    #####
    ....#
    ...##
    EOF
    puzzle.line_of_sight?({3,4}, {1,0}).should eq false
    puzzle.line_of_sight?({3,4}, {4,0}).should eq true

    puzzle.line_of_sight?({4,2}, {3,2}).should eq true
    puzzle.line_of_sight?({4,2}, {2,2}).should eq false


    puzzle = Puzzle.new
    puzzle.process <<-EOF
    ......#.#.
    #..#.#....
    ..#######.
    .#.#.###..
    .#..#.....
    ..#....#.#
    #..#....#.
    .##.#..###
    ##...#..#.
    .#....####
    EOF

    #puts "="*30
    puzzle.line_of_sight?({1,8}, {2,7}).should eq true
    puzzle.line_of_sight?({1,8}, {3,6}).should eq false
    puzzle.line_of_sight?({1,8}, {2,5}).should eq true
    puzzle.line_of_sight?({1,8}, {3,2}).should eq false
  end

  it "can calculate number in line of sight" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    .#..#
    .....
    #####
    ....#
    ...##
    EOF

    puzzle.map_los

    puzzle.los_count({4,2}).should eq 5
    puzzle.los_count({3,4}).should eq 8
  end

  it "can determine the best location" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    .#..#
    .....
    #####
    ....#
    ...##
    EOF

    puzzle.map_los

    loc, seen = puzzle.best()
    loc.should eq({3,4})
    seen.size.should eq 8
  end

  it "can sort visible by angle" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    .#....#####...#..
    ##...##.#####..##
    ##...#...#.#####.
    ..#.....#...###..
    ..#.#.....#....##
    EOF

    puzzle.map_los

    loc, visible = puzzle.best()

    #puts
    #puzzle.debug(loc)
    sorted = puzzle.sort(loc, visible)

    puzzle.sort(loc, sorted)

    sorted[0].should eq({8,1})
    sorted[1].should eq({9,0})
    sorted[2].should eq({9,1})
    sorted[3].should eq({10,0})
    sorted[4].should eq({9,2})
    sorted[5].should eq({11,1})
    sorted[6].should eq({12,1})
    sorted[7].should eq({11,2})
    sorted[8].should eq({15,1})
    
  end

end

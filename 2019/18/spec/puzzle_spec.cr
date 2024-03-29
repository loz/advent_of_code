require "spec"
require "./spec_helper"

describe Puzzle do

  it "parses a map" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    ########################
    #f.D.E.e.C.b.A.@.a.B.c.#
    ######################.#
    #d.....................#
    ########################
    EOF

    puzzle.start.should eq({15,1}) 
    puzzle.at(7,1).should eq 'e'
    puzzle.spaces.should eq 45
    puzzle.keys.should eq Set{'f','e','b','a','c','d'}
  end

  it "can determine where to explore" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    ########################
    #f.D.E.e.C.b.A.@.a.B.c.#
    ######################.#
    #d.....................#
    ########################
    EOF

    states = puzzle.new_candidates({ {15,1}, Set.new([] of Char )})
    states.size.should eq 2
    states.should contain({ {14,1} ,Set.new([] of Char)})
    states.should contain({ {16,1} ,Set.new([] of Char)})
  end

  it "does not consider door without key visitable" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    ########################
    #f.D.E.e.C.b.A.@.a.B.c.#
    ######################.#
    #d.....................#
    ########################
    EOF
    
    states = puzzle.new_candidates({ {14,1}, Set.new([] of Char) })
    states.should_not contain({ {13,1} , Set.new([] of Char) })
  end

  it "does consider door with its key visitable" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    ########################
    #f.D.E.e.C.b.A.@.a.B.c.#
    ######################.#
    #d.....................#
    ########################
    EOF
    
    states = puzzle.new_candidates({ {14,1}, Set.new(['a']) })
    states.should contain({ {13,1} ,Set.new(['a']) })
  end

  it "captures keys when present" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    ########################
    #f.D.E.e.C.b.A.@.a.B.c.#
    ######################.#
    #d.....................#
    ########################
    EOF
    
    states = puzzle.new_candidates({ {16,1}, Set.new([] of Char) })
    states.should contain({ {17,1} ,Set.new(['a']) })
  end

  it "can modify the map for robots" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    #######
    #a.#Cd#
    ##...##
    ##.@.##
    ##...##
    #cB#Ab#
    #######
    EOF

    puzzle.deploy_robots
    puzzle.robots.should contain({2,2})
    puzzle.robots.should contain({4,2})
    puzzle.robots.should contain({2,4})
    puzzle.robots.should contain({4,4})
    puzzle.at(3,2).should eq '#'
    puzzle.at(3,4).should eq '#'
    puzzle.at(2,3).should eq '#'
    puzzle.at(4,3).should eq '#'
    puzzle.at(3,3).should eq '#'
  end
end

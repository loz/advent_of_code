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

    states = puzzle.new_candidates({ {15,1}, [] of Char })
    states.size.should eq 2
    states.should contain({ {14,1} ,[] of Char})
    states.should contain({ {16,1} ,[] of Char})
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
    
    states = puzzle.new_candidates({ {14,1}, [] of Char })
    states.should_not contain({ {13,1} ,[] of Char})
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
    
    states = puzzle.new_candidates({ {14,1}, ['a'] })
    states.should contain({ {13,1} ,['a'] })
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
    
    states = puzzle.new_candidates({ {16,1}, [] of Char })
    states.should contain({ {17,1} ,['a'] })
  end
end

require "spec"
require "./spec_helper"

describe Layer do

  it "dies if not 1 bug adjacent" do
    layer = Layer.new
    layer.process <<-EOF
    #....
    .....
    .....
    .....
    .....
    EOF

    layer.at(0,0).should eq '#'
    layer.generation
    layer.at(0,0).should eq '.'
  end

  it "lives if 1 bug adjacent" do
    layer = Layer.new
    layer.process <<-EOF
    #....
    #....
    .....
    .....
    .....
    EOF

    layer.at(0,0).should eq '#'
    layer.generation
    layer.at(0,0).should eq '#'
  end

  it "infests empty if 1 or 2 bugs adjacent" do
    layer = Layer.new
    layer.process <<-EOF
    ##...
    #....
    .....
    ...#.
    .....
    EOF

    layer.generation
    layer.at(0,0).should eq '.'
    layer.at(1,1).should eq '#'
    layer.at(3,3).should eq '.'
    layer.at(2,3).should eq '#'
    layer.at(4,3).should eq '#'
    layer.at(3,2).should eq '#'
    layer.at(3,4).should eq '#'
  end

  it "matches example" do
    layer = Layer.new
    layer.process <<-EOF
    ....#
    #..#.
    #..##
    ..#..
    #....
    EOF
    layer.generation
    layer.dump.should eq <<-EOF
    #..#.
    ####.
    ###.#
    ##.##
    .##..
    EOF
  end

  it "calculates biodiversity rating" do
    layer = Layer.new
    layer.process <<-EOF
    ....#
    #..#.
    .....
    #....
    .#...
    EOF

    layer.diversity.should eq 16 + 32 + 256 + 32768 + 2097152
  end

  describe Puzzle do
    it "gives no neighbors for centergrid" do
      puzzle = Puzzle.new
      puzzle.process <<-EOF
      ....#
      #..#.
      #..##
      ..#..
      #....
      EOF
      puzzle.init_decks
    
      puzzle.neighbors(2,2,0).should eq( [] of Char)
    end

    it "calculates neighbors with inner left" do
      puzzle = Puzzle.new
      puzzle.process <<-EOF
      ....#
      #..#.
      #..##
      ..#..
      #....
      EOF
      puzzle.init_decks
      puzzle.neighbors(3,2,-1).count {|n| n == '#'}.should eq 2
    end

    it "calculates neighbors with inner right" do
      puzzle = Puzzle.new
      puzzle.process <<-EOF
      ....#
      #..#.
      #..##
      ..#..
      #....
      EOF
      puzzle.init_decks
      puzzle.neighbors(1,2,-1).count {|n| n == '#'}.should eq 3
    end


    it "calculates neighbors with inner bottom" do
      puzzle = Puzzle.new
      puzzle.process <<-EOF
      ....#
      #..#.
      #..##
      ..#..
      #####
      EOF
      puzzle.init_decks
      puzzle.neighbors(2,3,-1).count {|n| n == '#'}.should eq 5
    end

    it "calculates neighbors with inner top" do
      puzzle = Puzzle.new
      puzzle.process <<-EOF
      ....#
      #..#.
      #..##
      ..#..
      #####
      EOF
      puzzle.init_decks
      puzzle.neighbors(2,1,-1).count {|n| n == '#'}.should eq 1
    end

    it "calculates neighbors of outer top cells" do
      puzzle = Puzzle.new
      puzzle.process <<-EOF
      .....
      ..#..
      .#.#.
      .....
      .....
      EOF
      puzzle.init_decks
      (1..3).each do |x|
        puzzle.neighbors(x,0,1).count {|n| n == '#'}.should eq 1
      end
      puzzle.neighbors(0,0,1).count {|n| n == '#'}.should eq 2
      puzzle.neighbors(4,0,1).count {|n| n == '#'}.should eq 2
    end

    it "calculates neighbors of outer bottom cells" do
      puzzle = Puzzle.new
      puzzle.process <<-EOF
      .....
      .....
      .#.#.
      ..#..
      .....
      EOF
      puzzle.init_decks
      (1..3).each do |x|
        puzzle.neighbors(x,4,1).count {|n| n == '#'}.should eq 1
      end
      puzzle.neighbors(0,4,1).count {|n| n == '#'}.should eq 2
      puzzle.neighbors(4,4,1).count {|n| n == '#'}.should eq 2
    end

    it "calculates neighbors of outer left cells" do
      puzzle = Puzzle.new
      puzzle.process <<-EOF
      .....
      .....
      .#...
      .....
      .....
      EOF
      puzzle.init_decks
      (1..3).each do |y|
        puzzle.neighbors(0,y,1).count {|n| n == '#'}.should eq 1
      end
    end

    it "calculates neighbors of outer right cells" do
      puzzle = Puzzle.new
      puzzle.process <<-EOF
      .....
      .....
      ...#.
      .....
      .....
      EOF
      puzzle.init_decks
      (1..3).each do |y|
        puzzle.neighbors(4,y,1).count {|n| n == '#'}.should eq 1
      end
    end
  end
end

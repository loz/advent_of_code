require "spec"
require "./spec_helper"

describe Puzzle do

  it "considers potal spaces as neighbors" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
             A           
             A           
      #######.#########  
      #######.........#  
      #######.#######.#  
      #######.#######.#  
      #######.#######.#  
      #####  B    ###.#  
    BC...##  C    ###.#  
      ##.##       ###.#  
      ##...DE  F  ###.#  
      #####    G  ###.#  
      #########.#####.#  
    DE..#######...###.#  
      #.#########.###.#  
    FG..#########.....#  
      ###########.#####  
                 Z       
                 Z       
    EOF

    nexto = puzzle.neighbors({9,6})
    nexto.should contain({9,5})
    nexto.should contain({2,8})
  end

  it "does not consider external portals in level 0" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
             A           
             A           
      #######.#########  
      #######.........#  
      #######.#######.#  
      #######.#######.#  
      #######.#######.#  
      #####  B    ###.#  
    BC...##  C    ###.#  
      ##.##       ###.#  
      ##...DE  F  ###.#  
      #####    G  ###.#  
      #########.#####.#  
    DE..#######...###.#  
      #.#########.###.#  
    FG..#########.....#  
      ###########.#####  
                 Z       
                 Z       
    EOF

    nexto = puzzle.recursive_neighbors({0,{2,8}})
    nexto.should contain({0,{3,8}})
    nexto.should_not contain({-1,{9,6}})
    nexto.should_not contain({0,{9,6}})
    nexto.should_not contain({1,{9,6}})
  end

  it "considers internal portals in level 0, going to next level" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
             A           
             A           
      #######.#########  
      #######.........#  
      #######.#######.#  
      #######.#######.#  
      #######.#######.#  
      #####  B    ###.#  
    BC...##  C    ###.#  
      ##.##       ###.#  
      ##...DE  F  ###.#  
      #####    G  ###.#  
      #########.#####.#  
    DE..#######...###.#  
      #.#########.###.#  
    FG..#########.....#  
      ###########.#####  
                 Z       
                 Z       
    EOF

    nexto = puzzle.recursive_neighbors({0, {9,6}})
    nexto.should contain({0, {9,5}})
    nexto.should contain({1, {2,8}})
  end

  it "considers external portals in a level to go to the prior level" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
             A           
             A           
      #######.#########  
      #######.........#  
      #######.#######.#  
      #######.#######.#  
      #######.#######.#  
      #####  B    ###.#  
    BC...##  C    ###.#  
      ##.##       ###.#  
      ##...DE  F  ###.#  
      #####    G  ###.#  
      #########.#####.#  
    DE..#######...###.#  
      #.#########.###.#  
    FG..#########.....#  
      ###########.#####  
                 Z       
                 Z       
    EOF

    nexto = puzzle.recursive_neighbors({5,{2,8}})
    nexto.should contain({5,{3,8}})
    nexto.should contain({4,{9,6}})
  end

  it "locates start and end" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
             A           
             A           
      #######.#########  
      #######.........#  
      #######.#######.#  
      #######.#######.#  
      #######.#######.#  
      #####  B    ###.#  
    BC...##  C    ###.#  
      ##.##       ###.#  
      ##...DE  F  ###.#  
      #####    G  ###.#  
      #########.#####.#  
    DE..#######...###.#  
      #.#########.###.#  
    FG..#########.....#  
      ###########.#####  
                 Z       
                 Z       
    EOF

    puzzle.start.should eq({9,2})
    puzzle.finish.should eq({13,16})
  end

  it "locates inner and outer corners" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
             A           
             A           
      #######.#########  
      #######.........#  
      #######.#######.#  
      #######.#######.#  
      #######.#######.#  
      #####  B    ###.#  
    BC...##  C    ###.#  
      ##.##       ###.#  
      ##...DE  F  ###.#  
      #####    G  ###.#  
      #########.#####.#  
    DE..#######...###.#  
      #.#########.###.#  
    FG..#########.....#  
      ###########.#####  
                 Z       
                 Z       
    EOF

    outer = puzzle.outer_corners
    outer.should eq [{2,2},{18,16}]
    inner = puzzle.inner_corners
    inner.should eq [{6,6},{14,12}]
  end
end

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
end

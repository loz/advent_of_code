require 'minitest/autorun'
require_relative './reservoir'

describe Reservoir do
  before do
    @reservoir = Reservoir.new
    @example = <<-EOF
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
      EOF
  end

  describe "Water" do
    before do
      @example.each_line { |l| @reservoir.mark_vein(l)}
    end

    it "flows down" do
      w = Water.new()
      6.times { w.flow(@reservoir) }

      render = @reservoir.render_at(494,14,14)

      #puts "*"*20
      #puts @reservoir.colorize(render)
      #puts "*"*20

      render.must_equal <<-EOF
......+.......
......|.....#.
.#..#.|.....#.
.#..#.|#......
.#..#.|#......
.#....|#......
.#....|#......
.#######......
..............
..............
....#.....#...
....#.....#...
....#.....#...
....#######...
      EOF

    end

    it "flows left when it cannot flow down" do
      w = Water.new()
      7.times { w.flow(@reservoir) }

      render = @reservoir.render_at(494,14,14)

      #puts "*"*20
      #puts @reservoir.colorize(render)
      #puts "*"*20

      render.must_equal <<-EOF
......+.......
......|.....#.
.#..#.|.....#.
.#..#.|#......
.#..#.|#......
.#....|#......
.#...||#......
.#######......
..............
..............
....#.....#...
....#.....#...
....#.....#...
....#######...
      EOF
    end

    it "flows right when it cannot flow down" do
      w = Water.new()
      18.times { w.flow(@reservoir) }

      render = @reservoir.render_at(494,14,14)

      #puts "*"*20
      #puts @reservoir.colorize(render)
      #puts "*"*20

      render.must_equal <<-EOF
......+.......
......|.....#.
.#..#~|||...#.
.#..#~~#......
.#..#~~#......
.#~~~~~#......
.#~~~~~#......
.#######......
..............
..............
....#.....#...
....#.....#...
....#.....#...
....#######...
      EOF
    end

    it "rests if it cannot flow" do
      w = Water.new()
      11.times { w.flow(@reservoir) }

      render = @reservoir.render_at(494,14,14)

      #puts "*"*20
      #puts @reservoir.colorize(render)
      #puts "*"*20

      render.must_equal <<-EOF
......+.......
......|.....#.
.#..#.|.....#.
.#..#.|#......
.#..#.|#......
.#...||#......
.#~~~~~#......
.#######......
..............
..............
....#.....#...
....#.....#...
....#.....#...
....#######...
      EOF
    end

    it "detects complete flow" do
      w = Water.new()
      render = @reservoir.render_at(494,14)

      50.times { w.flow(@reservoir) }

      render = @reservoir.render_at(494,14)

      puts "*"*20
      puts @reservoir.colorize(render)
      puts "*"*20

      render.must_equal <<-EOF
......+.......
......|.....#.
.#..#~|||...#.
.#..#~~#|.....
.#..#~~#|.....
.#~~~~~#|.....
.#~~~~~#|.....
.#######|.....
........|.....
...|||||||||..
...|#~~~~~#|..
...|#~~~~~#|..
...|#~~~~~#|..
...*#######*..
      EOF

      w.must_be :complete?
    end
  end
  
  describe "mark_vein" do
    it "records veins vertically" do
      @reservoir.mark_vein("x=495, y=2..7")
      render = @reservoir.render_at(494,14,10)

      #puts "*"*20

      render.must_equal <<-EOF
......+.......
..............
.#............
.#............
.#............
.#............
.#............
.#............
..............
..............
      EOF
    end
    
    it "records veins in example" do
      @example.each_line { |l| @reservoir.mark_vein(l)}
      render = @reservoir.render_at(494,14,14)

      #puts "*"*20
      #puts @reservoir.colorize(render)
      #puts "*"*20

      render.must_equal <<-EOF
......+.......
............#.
.#..#.......#.
.#..#..#......
.#..#..#......
.#.....#......
.#.....#......
.#######......
..............
..............
....#.....#...
....#.....#...
....#.....#...
....#######...
      EOF
    end
  end
end

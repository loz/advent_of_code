require 'minitest/autorun'
require_relative './forrest'

describe Forrest do
  before do
    @forrest = Forrest.new
  end

  describe "grow" do
    describe "open space" do
      it "becomes filled with trees when 3 or more adjacent trees" do
        @forrest.set <<-EOF
||.
|..
...
        EOF
        @forrest.grow

        string = @forrest.string
        #puts "***"
        #puts @forrest.colorize(string)
        #puts "***"

        string.must_equal <<-EOF
||.
||.
...
        EOF
      end
    end

    describe "tree" do
      it "becomes a lumberyard if surrounded by 3 or more lumberyards" do
        @forrest.set <<-EOF
##.
#|.
...
        EOF
        @forrest.grow

        string = @forrest.string
        #puts "***"
        #puts @forrest.colorize(string)
        #puts "***"

        string.must_equal <<-EOF
##.
##.
...
        EOF
      end
    end

    describe "lumberyard" do
      it "becomes remains if surrounded by at least 1 tree and 1 lumberyard" do
        @forrest.set <<-EOF
||.
##.
...
        EOF
        @forrest.grow

        string = @forrest.string
        #puts "***"
        #puts @forrest.colorize(string)
        #puts "***"

        string.must_equal <<-EOF
||.
##.
...
        EOF
      end

      it "becomes open space if not" do
        @forrest.set <<-EOF
||.
|#.
...
        EOF
        @forrest.grow

        string = @forrest.string
        #puts "***"
        #puts @forrest.colorize(string)
        #puts "***"

        string.must_equal <<-EOF
||.
|..
...
        EOF
      end
    end

    it "grows according to the examples" do
      example = <<-EOF
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
      EOF
      @forrest.set example
      string = ""
      3.times { @forrest.grow }

      string = @forrest.string
      #puts "***"
      #puts @forrest.colorize(string)
      #puts "***"

      string.must_equal <<-EOF
.......#..
....|||#..
.|.||||...
..###|||.#
...##|||#|
.||##|||||
||||||||||
||||||||||
||||||||||
||||||||||
      EOF
    end
  end

  describe "value" do
    it "is total of wood * total lumber" do
      example = <<-EOF
.||##.....
||###.....
||##......
|##.....##
|##.....##
|##....##|
||##.####|
||#####|||
||||#|||||
||||||||||
      EOF

      @forrest.set example
      @forrest.value.must_equal 1147
    end
  end
end

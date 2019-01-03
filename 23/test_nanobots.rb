require 'minitest/autorun'
require_relative './nanobots'

describe Nanobots do
  before do
    @bots = Nanobots.new
  end

  it "can find the nanobot with the biggest range" do
    @bots.add("pos=<0,0,0>, r=4")
    @bots.add("pos=<4,0,0>, r=7")

    bot = @bots.greatest_range
    bot.pos.must_equal [4,0,0]
  end

  it "can find bots within range of a bot" do
    @bots.add("pos=<0,0,0>, r=4")

    @bots.add("pos=<4,0,0>, r=1")
    @bots.add("pos=<0,4,0>, r=1")
    @bots.add("pos=<0,0,4>, r=1")

    @bots.add("pos=<5,0,0>, r=1")
    @bots.add("pos=<0,5,0>, r=1")
    @bots.add("pos=<0,0,5>, r=1")

    @bots.add("pos=<2,2,0>, r=1")
    @bots.add("pos=<1,2,1>, r=1")

    target = @bots.bots.first
    nearest = @bots.nearest(target)

    nearest.count.must_equal 6
    positions = nearest.map &:pos

    positions.must_include [0,0,0]
    positions.must_include [2,2,0]
    positions.wont_include [5,0,0]
  end

  it "can provide a bounding box" do
    example = <<-EOF
pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5
    EOF
    example.each_line {|l| @bots.add(l) }

=begin
    /---/
   /---/|
   |   |/
   -----
=end

    box = @bots.bounding_box
    box.must_equal [10, 10, 10, 50, 50, 50]
  end

  it "calculates a center of a bounding box" do
    @bots.centre([10,10,10,50,50,50]).must_equal [
      30, 30, 30
    ]
  end

  it "subdivides a bounding box into 8 quadrants" do
    divisions = @bots.subdivide [10,10,10,50,50,50]
    divisions.must_equal [
      [10,10,10,30,30,30],
      [30,10,10,50,30,30],
      [10,30,10,30,50,30],
      [30,30,10,50,50,30],
      [10,10,30,30,30,50],
      [30,10,30,50,30,50],
      [10,30,30,30,50,50],
      [30,30,30,50,50,50],
    ]
  end

  it "calculates range correct for example" do
    example = <<-EOF
pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1
    EOF
    example.each_line {|l| @bots.add(l) }
    
    largest = @bots.greatest_range
    largest.range.must_equal 4

    nearest = @bots.nearest(largest)
    nearest.count.must_equal 7
  end

end

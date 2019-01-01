require 'minitest/autorun'
require_relative './cave'

describe Cave do
  before do
    @depth = 100
    @target = [10,10]
    @cave = Cave.new(@depth, @target)
  end

  it "has geological index of 0 at mouth" do
    @cave.geo_index(0,0).must_equal 0
  end

  it "has geological index of 0 at target" do
    @cave.geo_index(10,10).must_equal 0
  end

  it "has geo index of X * 16807 when Y == 0" do
    11.times do |x|
      @cave.geo_index(x,0).must_equal x * 16807
    end
  end

  it "has geo index of Y * 48271 when X == 0" do
    11.times do |y|
      @cave.geo_index(0,y).must_equal y * 48271
    end
  end

  it "has erosion level GIDX + DEPTH % 20183" do
    @cave.erosion_level(0,0).must_equal @depth
    @cave.erosion_level(10,10).must_equal @depth

    @cave.erosion_level(0,10).must_equal ((482710 + 100) % 20183)
    @cave.erosion_level(10,0).must_equal ((168070 + 100) % 20183)
  end

  it "has calculated geo and erosion index for Y and X > 0" do
    @cave.geo_index(1,1).must_equal 135340535
    @cave.erosion_level(1,1).must_equal 13620
  end

  it "has a calculated risk" do
    cave = Cave.new(3, [10,10])
    cave.risk(0,0).must_equal 0 #Rocky

    cave = Cave.new(4, [10,10])
    cave.risk(0,0).must_equal 1 #Wet

    cave = Cave.new(5, [10,10])
    cave.risk(0,0).must_equal 2 #Narrow
  end

  it "calculates total risk for depth and area to target" do
    cave = Cave.new(510, [10,10])
    cave.total_risk.must_equal 114
  end
end

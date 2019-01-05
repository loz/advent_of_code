require 'minitest/autorun'
require_relative './map'

describe Map do
  before do
    @map = Map.new
  end

  describe "#calculate_distance" do
    it "gives the distance between two points" do
      p1 = {x: 1, y:1}
      p2 = {x: 8, y:3}
      distance = @map.calculate_distance(p1,p2)
      distance.must_equal (7+2)
    end

    it "calculates distance irrespective of direction" do
      p1 = {x: 1, y:3}
      p2 = {x: 8, y:1}
      distance = @map.calculate_distance(p2,p1)
      distance.must_equal (7+2)
    end
  end

  describe "#finite_size" do
    it "gives the size based on the furthest away points on map" do
      size = @map.finite_size
      size.must_equal [0,0]

      @map.add_point({x:4, y:4})
      size = @map.finite_size
      size.must_equal [4,4]

      @map.add_point({x:2, y:8})
      size = @map.finite_size
      size.must_equal [4,8]
    end
  end

  describe "#distances_from_location" do
    it "gives the distance from a given location to each point on map" do
      a = {x: 1, y: 1}
      b = {x: 1, y: 6}
      c = {x: 8, y: 3}
      @map.add_point(a)
      @map.add_point(b)
      @map.add_point(c)
      
      distances = @map.distances_from_location(0,0)
      distances[a].must_equal 2
      distances[b].must_equal 7
      distances[c].must_equal 11
    end
  end

  describe "#closest_point_to_location" do
    it "gives the closest point to a location" do
      a = {x: 1, y: 1}
      b = {x: 1, y: 6}
      c = {x: 8, y: 3}
      @map.add_point(a)
      @map.add_point(b)
      @map.add_point(c)

      closest = @map.closest_point_to_location(0,0)
      closest.must_equal a
    end
    
    it "gives nopoint where no close point" do
      a = {x: 1, y: 1}
      b = {x: 1, y: 6}
      c = {x: 8, y: 3}
      @map.add_point(a)
      @map.add_point(b)
      @map.add_point(c)

      closest = @map.closest_point_to_location(6,6)
      closest.must_equal({nopoint: true})
    end
  end

  describe "when calculating areas" do
    before do
      @a = {x: 1, y: 1}
      @b = {x: 1, y: 6}
      @c = {x: 8, y: 3}
      @d = {x: 3, y: 4}
      @e = {x: 5, y: 5}
      @f = {x: 8, y: 9}
      @map.add_point(@a)
      @map.add_point(@b)
      @map.add_point(@c)
      @map.add_point(@d)
      @map.add_point(@e)
      @map.add_point(@f)
      @labels = {
        @a => 'a', @b => 'b', @c => 'c', @d => 'd',
        @e => 'e', @f => 'f', {nopoint: true} => '.'
        }
    end

    describe "#calculate_distance_sums" do
      it "calculates the sum of distance to all points for all parts of the finite map" do
        @map.calculate_distance_sums
        @map.dump_sum(32)

        @map.sum_at(4,3).must_equal 30
        @map.sum_below(32).must_equal 16
      end
    end

    describe "#calculate_grid" do
      it "calculates closest points for all parts of the finite map" do
        @map.calculate_grid

        @map.closest_at(0,0).must_equal @a
        @map.closest_at(3,2).must_equal @d
        @map.closest_at(8,6).must_equal({nopoint: true})
        @map.closest_at(4,7).must_equal @e
      end
    end

    describe "calculate_areas" do
      it "counts points on edges of finite as infinite" do
        @map.calculate_grid
        areas = @map.calculate_areas

        areas[@a].must_equal :infinity
        areas[@b].must_equal :infinity
        areas[@c].must_equal :infinity
        areas[@f].must_equal :infinity
      end

      it "counts total points allocated to grid" do
        @map.calculate_grid
        areas = @map.calculate_areas

        areas[@d].must_equal 9
        areas[@e].must_equal 17

        @map.dump(@labels)
      end
    end
  end
end

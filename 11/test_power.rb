require 'minitest/autorun'
require_relative './power'

describe Power do
  before do
    @power = Power.new
  end

  describe "#cell_power" do
    it "calculates correct power level for location and serial number" do
      @power.cell_power(3,5,8).must_equal 4
      @power.cell_power(122,79,57).must_equal -5
      @power.cell_power(217,196,39).must_equal 0
      @power.cell_power(101,153,71).must_equal 4
    end
  end

  describe "#build_cells" do
    it "calculates the cell power for all cells" do
      @power.build_cells(50,50,18) #5x5 with serial of 18

      @power.at(31 + 1, 43 + 1).must_equal -2
      @power.at(31 + 5, 43 + 2).must_equal -5
      @power.at(31 + 2, 43 + 3).must_equal 3
      @power.at(31 + 4, 43 + 4).must_equal 4
      @power.at(31 + 2, 43 + 5).must_equal 0

    end
  end

  describe "#calculate_grids" do
    it "calculates grid powers for all in 3x3 grids" do
      @power.build_cells(50,50,18)
      @power.calculate_grids(3)

      @power.grid_power_at(33,45).must_equal 29
    end

    it "can find largest grid" do
      @power.build_cells(50,50,18)
      @power.calculate_grids(3)
      
      @power.largest_grid.must_equal [33,45]
    end
  end
end

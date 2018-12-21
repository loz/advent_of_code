require 'minitest/autorun'
require_relative './fabric'

describe Fabric do
  before do
    @fabric = Fabric.new
  end

  describe "#parse_claim" do
    it "pulls out components of a claim" do
      claim = @fabric.parse_claim("#123 @ 3,2: 5x4")
      claim[:id].must_equal "#123"
      claim[:x].must_equal 3
      claim[:y].must_equal 2
      claim[:width].must_equal 5
      claim[:height].must_equal 4
    end
  end

end

require 'minitest/autorun'
require_relative './constelation'

describe Constelation do
  before do
    @stars = Constelation.new
  end

  it "creates a constelation from connected stars" do
    @stars.add("0,0,0,0")
    @stars.add("3,0,0,0")
    @stars.add("0,3,0,0")

    @stars.constelations.count.must_equal 1

    @stars.constelations.first.must_equal [
      [0,0,0,0],
      [3,0,0,0],
      [0,3,0,0]
    ]
  end

  it "creates more than one constelation when not connected" do
    @stars.add("0,0,0,0")
    @stars.add("3,0,0,0")
    @stars.add("0,3,0,0")

    @stars.add("9,0,0,0")
    @stars.add("12,0,0,0")
    @stars.constelations.count.must_equal 2

    @stars.constelations[1].must_equal [
      [9,0,0,0],
      [12,0,0,0],
    ]
  end

  it "joins constelations when star added which links" do
    @stars.add("0,0,0,0")
    @stars.add("3,0,0,0")
    @stars.add("0,3,0,0")
    @stars.add("0,0,3,0")
    @stars.add("0,0,0,3")
    @stars.add("0,0,0,6")

    @stars.add("9,0,0,0")
    @stars.add("12,0,0,0")
    @stars.constelations.count.must_equal 2

    @stars.add("6,0,0,0")

    @stars.constelations.count.must_equal 1
    @stars.constelations.first.length.must_equal 9
  end

end

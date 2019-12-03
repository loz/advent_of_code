require "spec"
require "./spec_helper"

describe Puzzle do

  it "calculates winner for given stats" do
    puzzle = Puzzle.new
    puzzle.boss(12, 7, 2)

    win = puzzle.fight(6,5,5)
    win.should eq false

    win = puzzle.fight(8,5,5)
    win.should eq true

    win = puzzle.fight(7,5,5)
    win.should eq true

    puzzle.boss(103,9,2)
    win = puzzle.fight(100, 7, 4)
    win.should eq false

  end

  it "caclulates the cheapest purchases" do
    puzzle = Puzzle.new
    puzzle.boss(12, 7, 2)

    items, cost = puzzle.cheapest(100)
    items.should contain "Dagger"
    cost.should eq 8
  end
end

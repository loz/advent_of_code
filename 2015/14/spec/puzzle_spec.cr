require "spec"
require "./spec_helper"

describe Puzzle do

  it "knows the stats for a reindeer" do
    puzzle = Puzzle.new
    puzzle.process "Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds."

    puzzle.speed("Comet").should eq 14
    puzzle.stamina("Comet").should eq 10
    puzzle.rest("Comet").should eq 127
  end

  it "calculates distance when flying" do
    puzzle = Puzzle.new
    puzzle.process "Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds."

    puzzle.distance_after(9, "Comet").should eq 14 * 9
  end

  it "calculates distance when resting" do
    puzzle = Puzzle.new
    puzzle.process "Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds."

    puzzle.distance_after(100, "Comet").should eq 14 * 10
  end
  
  it "calculates distance after resting" do
    puzzle = Puzzle.new
    puzzle.process "Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds."

    puzzle.distance_after(140, "Comet").should eq (14 * 10) + (14 * 3)
  end

  it "awards a point at a given second for the leader" do
    puzzle = Puzzle.new
    puzzle.process <<-EOF
    Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
    Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
    EOF
    scores = puzzle.points_at(1)
    scores["Comet"].should eq 0
    scores["Dancer"].should eq 1
  end
end

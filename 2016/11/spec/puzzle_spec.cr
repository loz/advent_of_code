require "spec"
require "./spec_helper"

describe Puzzle do

  describe "Possible Elevators" do
    it "generates the possible elevator filling for a floor" do
      puzzle = Puzzle.new
      options = puzzle.generate_lifts(Set.new([{:y, :microchip},{:y, :generator},{:z, :microchip}]))
      options.should contain(Set.new([{:z, :microchip}]))
      options.should contain(Set.new([{:y, :generator}]))
      options.should_not contain(Set.new([{:y, :microchip}]))
      options.should contain(Set.new([{:y, :microchip},{:y, :generator}]))
      options.should_not contain(Set.new([{:y, :generator}, {:z, :microchip}]))
      options.should_not contain(Set.new([{:z, :microchip}, {:y, :generator}]))

      options.size.should eq 4 #No Duplicates
    end
  end

  describe "Valid Floor States" do

    it "can tell that a lift can move" do
      puzzle = Puzzle.new
      puzzle.lift_can_move?(Set.new([{:x, :microchip}]), Set.new([{:y, :microchip}])).should eq true

    end

    it "can tell that a lift cannot move" do
      puzzle = Puzzle.new
      puzzle.lift_can_move?(Set.new([{:y, :microchip}]), Set.new([{:y, :generator},{:z, :microchip}])).should eq false
    end

    it "can tell if a lift can visit a floor" do
      puzzle = Puzzle.new
      puzzle.lift_can_visit?(Set.new([{:x, :microchip}]), Set.new([{:y, :microchip}])).should eq true
    end

    it "can tell if a lift can NOT visit a floor" do
      puzzle = Puzzle.new
      puzzle.lift_can_visit?(Set.new([{:x, :generator}]), Set.new([{:y, :microchip}])).should eq false
    end

    it "all initial states are valid" do
      puzzle = Puzzle.new
      elevator = Set.new([] of Tuple(Symbol,Symbol))

      Puzzle::INPUT.each do |f|
        puzzle.valid?(elevator, f).should eq true
      end
    end

    it "does not permit un-paired microchips on the same floor as a generator" do
      puzzle = Puzzle.new
      elevator = Set.new([] of Tuple(Symbol,Symbol))

      puzzle.valid?(elevator, Set.new([{:x, :microchip}, {:y, :generator}])).should eq false
    end

    it "does not permit un-paired microchips on the same floor as a generator including in elevator" do
      puzzle = Puzzle.new

      puzzle.valid?(Set.new([{:x, :microchip}]), Set.new([{:y, :generator}])).should eq false
      puzzle.valid?(Set.new([{:y, :generator}]), Set.new([{:x, :microchip}])).should eq false
    end

    it "does permit un-paired generators on the same floor as paired items" do
      puzzle = Puzzle.new

      puzzle.valid?(Set.new([{:x, :microchip}]), Set.new([{:x, :generator}, {:y, :generator}, {:z, :generator}])).should eq true
    end

    it "does permit all microchips on the floor / elevator" do
      puzzle = Puzzle.new
      elevator = Set.new([] of Tuple(Symbol,Symbol))

      puzzle.valid?(Set.new([{:x, :microchip}]), Set.new([{:y, :microchip}])).should eq true
      puzzle.valid?(elevator, Set.new([{:y, :microchip},{:x, :microchip}])).should eq true
    end

    it "does permit all generators on the floor / elevator" do
      puzzle = Puzzle.new
      elevator = Set.new([] of Tuple(Symbol,Symbol))

      puzzle.valid?(Set.new([{:x, :generator}]), Set.new([{:y, :generator}])).should eq true
      puzzle.valid?(elevator, Set.new([{:y, :generator},{:x, :generator}])).should eq true
    end

    it "does permit all paired items on the floor / elevator" do
      puzzle = Puzzle.new
      elevator = Set.new([] of Tuple(Symbol,Symbol))

      puzzle.valid?(Set.new([{:x, :generator}]), Set.new([{:x, :microchip}])).should eq true
      puzzle.valid?(elevator, Set.new([{:y, :microchip},{:y, :generator}])).should eq true
    end

    it "does permit unpaired microchips with all paired items on the floor / elevator" do
      puzzle = Puzzle.new
      elevator = Set.new([] of Tuple(Symbol,Symbol))

      puzzle.valid?(Set.new([{:x, :microchip}, {:y, :microchip}]), Set.new([{:x, :generator}])).should eq true
      puzzle.valid?(elevator, Set.new([{:y, :microchip},{:y, :generator},{:z, :microchip}])).should eq true
    end

    it "does not permit mix of items in the elevator" do
      puzzle = Puzzle.new
      elevator = Set.new([] of Tuple(Symbol,Symbol))

      puzzle.valid?(Set.new([{:x, :generator}, {:y, :microchip}]), Set.new([{:x, :microchip}])).should eq false
    end

  end
end

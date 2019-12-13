require "spec"
require "./spec_helper"

describe Puzzle do

  describe "Valid Floor States" do

    it "all initial states are valid" do
      puzzle = Puzzle.new
      elevator = [] of Tuple(Symbol,Symbol)

      Puzzle::INPUT.each do |f|
        puzzle.valid?(elevator, f).should eq true
      end
    end

    it "does not permit un-paired microchips on the same floor as a generator" do
      puzzle = Puzzle.new
      elevator = [] of Tuple(Symbol,Symbol)

      puzzle.valid?(elevator, [{:x, :microchip}, {:y, :generator}]).should eq false
    end

    it "does not permit un-paired microchips on the same floor as a generator including in elevator" do
      puzzle = Puzzle.new

      puzzle.valid?([{:x, :microchip}], [{:y, :generator}]).should eq false
      puzzle.valid?([{:y, :generator}], [{:x, :microchip}]).should eq false
    end

    it "does permit un-paired generators on the same floor as paired items" do
      puzzle = Puzzle.new

      puzzle.valid?([{:x, :microchip}], [{:x, :generator}, {:y, :generator}, {:z, :generator}]).should eq true
    end

    it "does permit all microchips on the floor / elevator" do
      puzzle = Puzzle.new
      elevator = [] of Tuple(Symbol,Symbol)

      puzzle.valid?([{:x, :microchip}], [{:y, :microchip}]).should eq true
      puzzle.valid?(elevator, [{:y, :microchip},{:x, :microchip}]).should eq true
    end

    it "does permit all generators on the floor / elevator" do
      puzzle = Puzzle.new
      elevator = [] of Tuple(Symbol,Symbol)

      puzzle.valid?([{:x, :generator}], [{:y, :generator}]).should eq true
      puzzle.valid?(elevator, [{:y, :generator},{:x, :generator}]).should eq true
    end

    it "does permit all paired items on the floor / elevator" do
      puzzle = Puzzle.new
      elevator = [] of Tuple(Symbol,Symbol)

      puzzle.valid?([{:x, :generator}], [{:x, :microchip}]).should eq true
      puzzle.valid?(elevator, [{:y, :microchip},{:y, :generator}]).should eq true
    end

    it "does permit unpaired microchips with all paired items on the floor / elevator" do
      puzzle = Puzzle.new
      elevator = [] of Tuple(Symbol,Symbol)

      puzzle.valid?([{:x, :microchip}, {:y, :microchip}], [{:x, :generator}]).should eq true
      puzzle.valid?(elevator, [{:y, :microchip},{:y, :generator},{:z, :microchip}]).should eq true
    end

    it "does not permit mix of items in the elevator" do
      puzzle = Puzzle.new
      elevator = [] of Tuple(Symbol,Symbol)

      puzzle.valid?([{:x, :generator}, {:y, :microchip}], [{:x, :microchip}]).should eq false
    end

  end
end

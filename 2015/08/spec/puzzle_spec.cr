require "spec"
require "./spec_helper"

describe Puzzle do

  it "counts string length including quotes" do
    puzzle = Puzzle.new
    puzzle.process(%{""})
    puzzle.string_length.should eq 2
  end

  it "counts memory length excluding quotes" do
    puzzle = Puzzle.new
    puzzle.process(%{""})
    puzzle.memory_length.should eq 0
  end

  it "counts string length including escaped characters" do
    puzzle = Puzzle.new
    puzzle.process(%q("aaa\"aaa"))
    puzzle.string_length.should eq 10
  end

  it "counts memory length excluding escape character" do
    puzzle = Puzzle.new
    puzzle.process(%q("aaa\"aaa"))
    puzzle.memory_length.should eq 7
  end

  it "counts string length including hex characters" do
    puzzle = Puzzle.new
    puzzle.process(%q("\x27"))
    puzzle.string_length.should eq 6
  end

  it "counts memory length evaling hex characters" do
    puzzle = Puzzle.new
    puzzle.process(%q("\x27"))
    puzzle.memory_length.should eq 1
  end

  it "counts string length excluding whitespace" do
    puzzle = Puzzle.new
    puzzle.process(%q("abc"
"\x27"))
    puzzle.string_length.should eq 11
  end
end
